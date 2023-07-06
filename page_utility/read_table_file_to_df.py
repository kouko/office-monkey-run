import pandas as pd
from collections import defaultdict


def read_table_file_to_df(table_file, header_row_from=1, header_row_to=1, dtype: dict = {}, default_dtype: type = None) -> pd.DataFrame:
    """

    :param table_file:
    :param header_row_from:
    :param header_row_to:
    :param dtype:
    :param default_dtype: 設定預設的資料型態，如果為了要保持原有值的外觀，建議設定為 pd.StringDtype， str 可能會有點問題
    :return:
    """

    dtype_dict = defaultdict(default_dtype, **dtype) if default_dtype is not None else dtype
    keep_default_na = False if default_dtype is not None else True
    header_index_list = list(range(header_row_from-1, header_row_to))

    if table_file is None:
        return None
    else:
        if table_file.type == 'text/csv':
            read_df = pd.read_csv(table_file, header=header_index_list, encoding_errors='ignore', dtype=dtype_dict, keep_default_na=keep_default_na)
        elif table_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            read_df = pd.read_excel(table_file, header=header_index_list, dtype=dtype_dict, keep_default_na=keep_default_na)
        else:
            raise TypeError(f'table_file type error: {table_file.type}')

    if keep_default_na is False:
        read_df.replace(to_replace='', value=None, inplace=True)

    # 只有 index 被指定超過 1 row 時才要特殊處理
    if len(header_index_list) > 1:
        column_name_df = pd.DataFrame(read_df.columns.tolist())
        column_name_df = column_name_df.astype(str)
        column_name_df.replace(to_replace='^Unnamed.*$', value=None, regex=True, inplace=True)
        column_name_df.replace(to_replace='', value=None, regex=False, inplace=True)
        column_name_df.fillna(method='ffill', inplace=True)
        for idx in column_name_df.index.tolist():
            column_name_df.loc[idx] = column_name_df.loc[idx].fillna(str(idx))

        # st.dataframe(column_name_df)
        new_column_name_array = column_name_df.values.tolist()
        new_column_name_list = ['>'.join(new_column_name_l) for new_column_name_l in new_column_name_array]
        read_df.columns = new_column_name_list
    return read_df