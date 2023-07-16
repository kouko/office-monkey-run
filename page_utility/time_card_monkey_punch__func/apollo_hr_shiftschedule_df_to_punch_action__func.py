import pandas as pd


def apollo_hr_shiftschedule_df_to_punch_action(shift_schedule_df: pd.DataFrame, month: str) -> (pd.DataFrame, pd.DataFrame):

    shift_schedule__punch_action_df = shift_schedule_df[~shift_schedule_df['on_duty'].isna()].copy()
    shift_schedule__punch_action_df = shift_schedule__punch_action_df.melt(
        id_vars=['day', 'day_type', 'schedule_name', 'note'],
        value_vars=['on_duty', 'off_duty'],
        var_name='punch_type',
        value_name='time')

    shift_schedule__punch_action_df.sort_values(by=['day', 'time'], inplace=True, ignore_index=True)
    shift_schedule__punch_action_df['punch_time'] = month + '-' + shift_schedule__punch_action_df['day'].astype(str).str.zfill(2) + ' ' + shift_schedule__punch_action_df['time'].astype(str)
    debug_df = shift_schedule__punch_action_df.copy()
    punch_action_df = shift_schedule__punch_action_df[['punch_time', 'punch_type']].copy()
    return punch_action_df, debug_df

