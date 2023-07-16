import re
import pandas as pd


def apollo_hr_shiftschedule_text_to_dataframe(shift_schedule: str) -> pd.DataFrame:
    """
    INPUT:
        text copy from table in page : https://apollo.mayohr.com/ta/personal/shiftschedule

    OUTPUT COLUMN:
        - day: 日期
        - day_type: 例假日/休息日/國定假日/工作日
        - schedule_name: 班別名稱
        - on_duty: 上班時間
        - off_duty: 下班時間
        - note: 備註

    :param shift_schedule:
    :return:
    """

    # ============================================
    # 處理 INPUT schedule 轉換為 陣列
    # ============================================
    shift_schedule__cleaned = re.sub(r'[\r\n]+', r'\n', shift_schedule)
    shift_schedule__with_split_mark = re.sub(r'(^[0-9]{2}$|^日\t一)', r'==\1', shift_schedule__cleaned, flags=re.MULTILINE)
    # print(shift_schedule__with_split_mark)
    shift_schedule__line_list = shift_schedule__with_split_mark.split('==')
    shift_schedule__line_list = [line.strip().split('\n') for line in shift_schedule__line_list]

    shift_schedule_dict_list = []
    for line in shift_schedule__line_list:
        first_element_is_day = bool(re.search(r'^[0-9]{2}$', line[0]))
        line_len = len(line)
        last_element_is_period = bool(re.search(r'^[0-9]{2}:[0-9]{2}~[0-9]{2}:[0-9]{2}$', line[-1]))
        last_element_is_off = bool(re.search(r'例假日|休息日|國定假日|flexible rest day|One fixed day off|National holiday', line[-1]))
        if first_element_is_day and last_element_is_off and line_len == 3:
            day_dict = {
                'day': int(line[0]),
                'day_type': line[2],
                'schedule_name': line[1],
                'on_duty': None,
                'off_duty': None,
                'note': None,
            }
            shift_schedule_dict_list.append(day_dict)
        elif first_element_is_day and last_element_is_off and line_len == 4:
            day_dict = {
                'day': int(line[0]),
                'day_type': line[3],
                'schedule_name': line[2],
                'on_duty': None,
                'off_duty': None,
                'note': line[1],
            }
            shift_schedule_dict_list.append(day_dict)
        elif first_element_is_day and last_element_is_period:
            day_dict = {
                'day': int(line[0]),
                'day_type': '工作日',
                'schedule_name': line[1],
                'on_duty': line[-1].split('~')[0],
                'off_duty': line[-1].split('~')[1],
                'note': None,
            }
            shift_schedule_dict_list.append(day_dict)
        else:
            pass

    shift_schedule_df = pd.DataFrame(shift_schedule_dict_list)
    return shift_schedule_df


""" INPUT SAMPLE
日	一	二	三	四	五	六
01
常日班(六休日例)
例假日
02
元旦
常日班(六休日例)
國定假日
03
常日班(六休日例)
09:30~18:30
04
常日班(六休日例)
09:30~18:30
05
常日班(六休日例)
09:30~18:30
06
常日班(六休日例)
09:30~18:30
07
常日班(六休日例)
休息日
08
常日班(六休日例)
例假日
09
常日班(六休日例)
09:30~18:30
10
常日班(六休日例)
09:30~18:30
11
常日班(六休日例)
09:30~18:30
12
常日班(六休日例)
09:30~18:30
13
常日班(六休日例)
09:30~18:30
14
常日班(六休日例)
休息日
15
常日班(六休日例)
例假日
16
常日班(六休日例)
09:30~18:30
17
常日班(六休日例)
09:30~18:30
18
常日班(六休日例)
09:30~18:30
19
常日班(六休日例)
09:30~18:30
20
農曆春節
常日班(六休日例)
休息日
21
常日班(六休日例)
休息日
22
常日班(六休日例)
例假日
23
農曆春節
常日班(六休日例)
國定假日
24
農曆春節
常日班(六休日例)
國定假日
25
農曆春節
常日班(六休日例)
國定假日
26
農曆春節
常日班(六休日例)
國定假日
27
農曆春節
常日班(六休日例)
休息日
28
常日班(六休日例)
休息日
29
常日班(六休日例)
例假日
30
常日班(六休日例)
09:30~18:30
31
常日班(六休日例)
09:30~18:30
01
02
03
04

"""