import pandas as pd


def apollo_hr_leave_list_df_to_punch_action(leave_list_df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    leave_list__punch_action_df = leave_list_df.copy()
    leave_list__punch_action_df = leave_list__punch_action_df.melt(
        id_vars=['ticker_no', 'effect_start_date', 'effect_end_date'],
        value_vars=['on_leave', 'off_leave'],
        var_name='punch_type',
        value_name='punch_time')
    leave_list__punch_action_df['punch_time'] = leave_list__punch_action_df['punch_time'].str.replace('/', '-')
    debug_df = leave_list__punch_action_df.copy()
    punch_action_df = leave_list__punch_action_df[['punch_time', 'punch_type']]
    return punch_action_df, debug_df

