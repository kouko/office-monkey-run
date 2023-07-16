import pandas as pd


def apollo_hr_shiftschedule_punch_action_to_break_punch_action(shift_schedule__punch_action_df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    shift_day_list = pd.to_datetime(shift_schedule__punch_action_df['punch_time']).dt.date.unique()
    break_df = pd.DataFrame({'date': shift_day_list, 'on': '12:30', 'off': '13:30'})
    break_df['on_break'] = break_df['date'].astype(str) + ' ' + break_df['on']
    break_df['off_break'] = break_df['date'].astype(str) + ' ' + break_df['off']
    break__punch_action_df = break_df.melt(
        id_vars=None,
        value_vars=['on_break', 'off_break'],
        var_name='punch_type',
        value_name='punch_time'
    )
    debug_df = break__punch_action_df.copy()
    punch_action_df = break__punch_action_df[['punch_time', 'punch_type']]
    return punch_action_df, debug_df

