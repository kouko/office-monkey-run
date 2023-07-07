import streamlit as st
import pandas as pd
from page_utility import read_table_file_to_df


# ==============================================
# 設定 Page Config
# ==============================================
st.set_page_config(page_title='OfficeMonkeyRun : GroupByMonkeyAgg',
                   page_icon=':monkey_face:',
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

# ==============================================
# Read Table File
# ==============================================
@st.cache_data
def read_table_file(table_file, header_row_from=1, header_row_to=1) -> pd.DataFrame:
    read_df = read_table_file_to_df(table_file=table_file,
                                    header_row_from=header_row_from, header_row_to=header_row_to)
    return read_df


# ==============================================
# Page Title
# ==============================================
st.title('GroupByMonkeyAgg')


# ==============================================
# Upload File
# ==============================================
st.header('01 Upload Table Files')
uploaded_table_file = st.file_uploader(label='Left Table', type=['csv', 'xlsx'], key='duplicated_drop_file', accept_multiple_files=False)
if uploaded_table_file is not None:
    left_table__header_row__column_1, left_table__header_row__column_2 = st.columns(2)
    with left_table__header_row__column_1:
        left_table__header_row_from = st.number_input(label='Column Name From Row : ', min_value=1, max_value=None, value=1, step=1, key='left_table_row_from')
    with left_table__header_row__column_2:
        left_table__header_row_to = st.number_input(label='Column Name To Row : ', min_value=1, max_value=None, value=1, step=1, key='left_table_row_to')
    table_file_df = read_table_file(table_file=uploaded_table_file, header_row_from=left_table__header_row_from, header_row_to=left_table__header_row_to)
    st.dataframe(table_file_df, use_container_width=True)
else:
    st.info('Please upload table files first.')
    table_file_df = pd.DataFrame()
    st.stop()


# ==============================================
# Select Columns for Groupby
# ==============================================
st.header('02 Set Columns for Groupby')
if table_file_df.empty:
    st.info('Please upload table files first.')
    groupby_column_list = None
    st.stop()
else:
    groupby_column_list = st.multiselect(label='Columns for Groupby : ',
                                         options=table_file_df.columns.tolist(),
                                         default=None,
                                         key='left_table_groupby_column')

# ==============================================
# Select Columns for Aggregation
# ==============================================
st.header('03 Set Columns for Aggregation')
if table_file_df.empty:
    st.info('Please upload table files first.')
    final_agg_setting_df = pd.DataFrame()
    st.stop()
else:
    table_file_columns = table_file_df.columns.tolist()

    agg_available_columns = [column for column in table_file_columns if column not in groupby_column_list]

    agg_setting_df = pd.DataFrame(
        {'Column': [None, None, None],
        'Aggregation': [None, None, None]}
    )
    agg_setting_df['Column'] = agg_setting_df['Column'].astype('category').cat.add_categories(agg_available_columns)
    agg_setting_df['Aggregation'] = agg_setting_df['Aggregation'].astype('category').cat.add_categories(['SUM', 'MEAN', 'MAX', 'MIN', 'COUNT', 'NUNIQUE'])

    edited_agg_setting_df = st.data_editor(agg_setting_df, num_rows='dynamic', use_container_width=True)
    final_agg_setting_df = edited_agg_setting_df.copy()
    final_agg_setting_df.dropna(axis=0, inplace=True)

# ==============================================
# Agg
# ==============================================
st.header('04 Aggregation')
if groupby_column_list is None or final_agg_setting_df.empty:
    st.info('Please set columns for groupby and aggregation.')
    st.stop()
elif len(groupby_column_list) == 0 or len(final_agg_setting_df) == 0:
    st.info('Please set columns for groupby and aggregation.')
    st.stop()
else:
    agg_dict = final_agg_setting_df.to_dict(orient='records')

    agg_df_list = []
    for agg in agg_dict:
        agg_column = agg['Column']
        agg_method = agg['Aggregation']
        agg_series = table_file_df.groupby(groupby_column_list)[agg_column].agg(agg_method.lower())
        agg_series.name = f'{agg_column}_{agg_method}'
        agg_df_list.append(agg_series)

    all_agg_df = pd.concat(agg_df_list, axis=1)
    st.dataframe(all_agg_df, use_container_width=True)

    csv = all_agg_df.to_csv(index=False).encode('utf-8')
    filename = f'GroupBy_Agg.csv'
    st.download_button(label='Download CSV', data=csv, file_name=filename, mime='text/csv', key='download_csv', use_container_width=True)