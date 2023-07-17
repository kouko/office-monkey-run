import pandas as pd
import random


def apollp_hr_punch_log_random_engine(punch_log_df:pd.DataFrame, random_mode: str, random_range: int):
    """ 隨機重編 TS

    :param punch_log_df:
    :param random_mode:
    :param random_range:
    :return:
    """
    log_df = punch_log_df.copy()

    log_df['_ORIGINAL_TS'] = pd.to_datetime(log_df['*打卡日期(YYYY/MM/DD)'] + ' ' + log_df['*打卡時間(HH:mm)'])
    log_df['_RANDOM_TS'] = log_df['_ORIGINAL_TS']
    if random_mode == 'Simple Random':
        for idx, row in log_df.iterrows():
            if idx == 0:
                previous_diff_minutes = random_range
                next_diff_minutes = (log_df.loc[idx+1]['_RANDOM_TS'] - log_df.loc[idx]['_RANDOM_TS']) / pd.Timedelta(minutes=1)
            elif idx == len(log_df) - 1:
                previous_diff_minutes = (log_df.loc[idx]['_RANDOM_TS'] - log_df.loc[idx-1]['_RANDOM_TS']) / pd.Timedelta(minutes=1)
                next_diff_minutes = random_range
            else:
                previous_diff_minutes = (log_df.loc[idx]['_RANDOM_TS'] - log_df.loc[idx-1]['_RANDOM_TS']) / pd.Timedelta(minutes=1)
                next_diff_minutes = (log_df.loc[idx+1]['_RANDOM_TS'] - log_df.loc[idx]['_RANDOM_TS']) / pd.Timedelta(minutes=1)

            final_random_range = min(random_range, min(previous_diff_minutes, next_diff_minutes)) - 1
            final_random_minutes = random.randint(final_random_range * -1, final_random_range)

            log_df.loc[idx, '_RANDOM_TS'] = log_df.loc[idx]['_RANDOM_TS'] + pd.Timedelta(minutes=final_random_minutes)
    else:
        pass

    log_df['*打卡日期(YYYY/MM/DD)'] = log_df['_RANDOM_TS'].dt.strftime('%Y/%m/%d')
    log_df['*打卡時間(HH:mm)'] = log_df['_RANDOM_TS'].dt.strftime('%H:%M')
    output_columns = [
        '*工號',
        '姓名',
        '*類型(1=上班，2=下班，3=休息開始，4=休息結束)',
        '*打卡日期(YYYY/MM/DD)',
        '*打卡時間(HH:mm)',
        '*地點',
        '事由(字數限制 250 字)',
    ]
    random_log_df = log_df[output_columns].copy()
    debug_df = log_df
    return random_log_df, debug_df
