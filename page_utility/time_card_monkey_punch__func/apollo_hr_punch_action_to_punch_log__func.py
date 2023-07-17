import pandas as pd


def apollo_hr_punch_action_to_punch_log(
        punch_action_df_list: list[pd.DataFrame],
        employee_no: str,
        month: str,
        employee_name: str,
        location: str
    ) -> (pd.DataFrame, pd.DataFrame):

    # ==============================================
    # Combine punch_log_df
    # ==============================================
    punch_action_df = pd.concat(punch_action_df_list, axis=0, ignore_index=True)
    punch_action_df.sort_values(by=['punch_time'], inplace=True, ignore_index=True)
    punch_action_df = punch_action_df.pivot(
        index='punch_time',
        columns='punch_type',
        values='punch_type'
    ).reset_index(drop=False)
    punch_action_df.sort_values(by=['punch_time'], inplace=True, ignore_index=True)
    punch_action_df.insert(loc=0, column='punch_date', value=pd.to_datetime(punch_action_df['punch_time']).dt.date)
    on_off_columns = ['on_duty', 'off_duty', 'on_break', 'off_break', 'on_leave', 'off_leave']
    for column in on_off_columns:
        if column not in punch_action_df.columns:
            punch_action_df[column] = None
    punch_action_df = punch_action_df[['punch_date', 'punch_time'] + on_off_columns]

    # ==============================================
    # Filter data by month
    # ==============================================

    month_filter = pd.to_datetime(punch_action_df['punch_date']).dt.strftime('%Y-%m') == month
    punch_action_df = punch_action_df[month_filter].copy()

    # ==============================================
    # State Analytics
    # ==============================================
    def state_analytics(row, on_column, off_column):
        if row[on_column] == on_column:
            return True
        elif row[off_column] == off_column:
            return False
        else:
            return None

    punch_action_df['duty'] = punch_action_df.apply(lambda x: state_analytics(x, on_column='on_duty', off_column='off_duty'), axis=1)
    punch_action_df['duty'] = punch_action_df['duty'].fillna(method='ffill')

    punch_action_df['break'] = punch_action_df.apply(lambda x: state_analytics(x, on_column='on_break', off_column='off_break'), axis=1)
    punch_action_df['break'] = punch_action_df['break'].fillna(method='ffill')

    punch_action_df['leave'] = punch_action_df.apply(lambda x: state_analytics(x, on_column='on_leave', off_column='off_leave'), axis=1)
    punch_action_df['leave'] = punch_action_df['leave'].fillna(method='ffill')

    def agg_state(row):
        if row['leave'] is True:
            return 'off'
        elif row['break'] is True:
            return 'break'
        elif row['duty'] is True:
            return 'duty'
        else:
            return 'off'

    punch_action_df['status'] = punch_action_df.apply(lambda x: agg_state(x), axis=1)

    # ==========================================
    # Clean Status (當 off 與 break 相連時， break=off)
    # ==========================================
    for idx, row in punch_action_df.iterrows():
        if row['status'] == 'break' and punch_action_df.loc[idx + 1, 'status'] == 'off':
            punch_action_df.loc[idx, 'clean_status'] = 'off'

        elif row['status'] == 'break' and punch_action_df.loc[idx - 1, 'status'] == 'off':
                punch_action_df.loc[idx, 'clean_status'] = 'off'
        else:
            punch_action_df.loc[idx, 'clean_status'] = row['status']

    punch_action_df['previous_clean_status'] = punch_action_df.groupby('punch_date')['clean_status'].shift(1)

    # ==========================================
    # punch action
    # ==========================================

    def punch(row):
        if row['previous_clean_status'] == row['clean_status']:
            return None
        elif pd.isnull(row['previous_clean_status']) and row['clean_status'] == 'duty':
            return 'punch__on_duty'
        elif row['previous_clean_status'] == 'off' and row['clean_status'] == 'duty':
            return 'punch__on_duty'
        elif row['previous_clean_status'] == 'break' and row['clean_status'] == 'duty':
            return 'punch__off_break'

        elif row['previous_clean_status'] == 'duty' and row['clean_status'] == 'break':
            return 'punch__on_break'

        elif pd.isnull(row['previous_clean_status']) and row['clean_status'] == 'off':
            return None
        elif row['previous_clean_status'] == 'duty' and row['clean_status'] == 'off':
            return 'punch__off_duty'
        else:
            return None


    punch_action_df['punch'] = punch_action_df.apply(lambda x: punch(x), axis=1)

    # ==========================================
    # punch log
    # ==========================================

    punch_log_df = punch_action_df.dropna(subset=['punch'], ignore_index=True)[['punch_time', 'punch']].copy()
    punch_map = {
        'punch__on_duty': 1,
        'punch__off_duty': 2,
        'punch__on_break': 3,
        'punch__off_break': 4
    }
    punch_log_df['*工號'] = employee_no
    punch_log_df['姓名'] = employee_name
    punch_log_df['*類型(1=上班，2=下班，3=休息開始，4=休息結束)'] = punch_log_df['punch'].map(punch_map)
    punch_log_df['*打卡日期(YYYY/MM/DD)'] = pd.to_datetime(punch_log_df['punch_time']).dt.strftime('%Y/%m/%d')
    punch_log_df['*打卡時間(HH:mm)'] = pd.to_datetime(punch_log_df['punch_time']).dt.strftime('%H:%M')
    punch_log_df['*地點'] = location
    punch_log_df['事由(字數限制 250 字)'] = ''

    output_columns = [
        '*工號',
        '姓名',
        '*類型(1=上班，2=下班，3=休息開始，4=休息結束)',
        '*打卡日期(YYYY/MM/DD)',
        '*打卡時間(HH:mm)',
        '*地點',
        '事由(字數限制 250 字)',
    ]
    punch_log_df = punch_log_df[output_columns]

    return punch_log_df, punch_action_df
