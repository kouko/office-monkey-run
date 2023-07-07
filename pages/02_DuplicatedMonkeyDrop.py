import streamlit as st
import pandas as pd
from page_utility import read_table_file_to_df


# ==============================================
# 設定 Page Config
# ==============================================
st.set_page_config(page_title='OfficeMonkeyRun : DuplicatedMonkeyDrop',
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
                                    header_row_from=header_row_from, header_row_to=header_row_to,
                                    default_dtype=pd.StringDtype)
    return read_df

# ==============================================
# UI
# ==============================================

st.title('DuplicatedMonkeyDrop')

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

st.header('02 Set Columns for duplicated check')
if uploaded_table_file is None:
    st.info('Please upload table files first.')
    duplicated_check_column_list = []
    st.stop()
else:
    duplicated_check_column_list = st.multiselect(label='Columns for duplicated check : ', options=table_file_df.columns.tolist(), default=None, key='left_table_duplicated_check_column')

st.header('03 Set Mode')
mode = st.selectbox(label='Mode : ', options=['Drop Duplicated', 'Only Duplicated'], index=0, key='mode')


st.header('04 Result')
if len(duplicated_check_column_list) == 0:
    st.info('Please upload table files first.')
    result_df = pd.DataFrame()
    st.stop()
elif mode == 'Drop Duplicated':
    result_df = table_file_df.drop_duplicates(subset=duplicated_check_column_list, keep='first')
elif mode == 'Only Duplicated':
    duplicated_filter = table_file_df.duplicated(subset=duplicated_check_column_list, keep=False)
    result_df = table_file_df[duplicated_filter]
    result_df.dropna(subset=duplicated_check_column_list, inplace=True)
    result_df.sort_values(by=duplicated_check_column_list, inplace=True)
else:
    st.error('Unknown Mode : {}'.format(mode))
    result_df = pd.DataFrame()
    st.stop()
st.dataframe(result_df, use_container_width=True)
csv = result_df.to_csv(index=False).encode('utf-8')
filename = 'drop_duplicated.csv' if mode == 'Drop Duplicated' else 'only_duplicated.csv'
st.download_button(label='Download CSV', data=csv, file_name=filename, mime='text/csv', key='download_csv', use_container_width=True)