import pandas as pd
import re


def apollo_hr_leave_list_text_to_dataframe(leave_list: str) -> pd.DataFrame:
    # ============================================
    # 處理 INPUT schedule 轉換為 List
    # ============================================
    leave_list__cleaned = re.sub(r'[\r\n]+', r'\n', leave_list)
    leave_list__line_list = leave_list__cleaned.split('\n')

    # ============================================
    # 解析每一行資料
    # ============================================
    line_data_dict_list = []
    for line in leave_list__line_list:
        line_clean = line.strip()
        line_clean = re.sub(r'[\s\t]+', r' ', line_clean)
        # print(repr(line_clean))
        line_is_title = bool(re.search('有效期限', line_clean))
        line_is_empty = bool(re.search('^\s*$', line_clean))
        date_regex = r'(\d{4}/\d{2}/\d{2})'
        ticker_regex = r'([^\s\t]+)'
        datetime_regex = r'(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})'
        period_regex = r'(\d+)\s時\s(\d+)\s分'
        period_regex_en = r'(\d+)\shr\s(\d+)\smin'
        full_regex = f'^{date_regex}\s~\s{date_regex}\s{ticker_regex}\s{datetime_regex}\s~\s{datetime_regex}\s{period_regex}$'
        full_regex_en = f'^{date_regex}\s~\s{date_regex}\s{ticker_regex}\s{datetime_regex}\s~\s{datetime_regex}\s{period_regex_en}$'
        line_is_leave_data = bool(re.search(full_regex, line_clean))
        line_is_leave_data_en = bool(re.search(full_regex_en, line_clean))

        # print(line_is_title, line_is_empty, line_is_leave_data)

        if line_is_title:
            pass
        elif line_is_empty:
            pass
        elif line_is_leave_data or line_is_leave_data_en:
            line_regex = full_regex if line_is_leave_data else full_regex_en
            leave_data_dict = {
                'effect_start_date': re.search(line_regex, line_clean).group(1),
                'effect_end_date': re.search(line_regex, line_clean).group(2),
                'ticker_no': re.search(line_regex, line_clean).group(3),
                'on_leave': re.search(line_regex, line_clean).group(4),
                'off_leave': re.search(line_regex, line_clean).group(5),
                'period_hour': re.search(line_regex, line_clean).group(6),
                'period_minute': re.search(line_regex, line_clean).group(7)
            }
            line_data_dict_list.append(leave_data_dict)
    line_data_df = pd.DataFrame(line_data_dict_list)
    return line_data_df


""" INPUT SAMPLE
有效期限	表單號	請假區間	時數
2022/04/01 ~ 2024/03/31	135	2023/07/21 13:30 ~ 2023/07/21 18:30	5 時 0 分
2022/04/01 ~ 2024/03/31	137	2023/08/09 09:30 ~ 2023/08/09 18:30	8 時 0 分
"""