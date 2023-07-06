import streamlit as st
import pandas as pd
from page_utility import read_table_file_to_df


# ==============================================
# 設定 Page Config
# ==============================================
st.set_page_config(page_title='OfficeMonkeyRun : TableMonkeyJoin',
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

st.title('TableMonkeyJoin')

st.header('01 Upload Table Files')
left_table_column, right_table_column = st.columns(2)
with left_table_column:
    left_table_file = st.file_uploader(label='Left Table', type=['csv', 'xlsx'], key='left_table', accept_multiple_files=False)
    if left_table_file is not None:
        left_table__header_row__column_1, left_table__header_row__column_2 = st.columns(2)
        with left_table__header_row__column_1:
            left_table__header_row_from = st.number_input(label='Column Name From Row : ', min_value=1, max_value=None, value=1, step=1, key='left_table_row_from')
        with left_table__header_row__column_2:
            left_table__header_row_to = st.number_input(label='Column Name To Row : ', min_value=1, max_value=None, value=1, step=1, key='left_table_row_to')
        left_df = read_table_file(table_file=left_table_file, header_row_from=left_table__header_row_from, header_row_to=left_table__header_row_to)
        st.dataframe(left_df)

with right_table_column:
    right_table_file = st.file_uploader(label='Right Table', type=['csv', 'xlsx'], key='right_table', accept_multiple_files=False)
    if right_table_file is not None:
        right_table__header_row__column_1, right_table__header_row__column_2 = st.columns(2)
        with right_table__header_row__column_1:
            right_table__header_row_from = st.number_input(label='Column Name From Row : ', min_value=1, max_value=None, value=1, step=1, key='right_table_row_from')
        with right_table__header_row__column_2:
            right_table__header_row_to = st.number_input(label='Column Name To Row : ', min_value=1, max_value=None, value=1, step=1, key='right_table_row_to')
        right_df = read_table_file(table_file=right_table_file, header_row_from=right_table__header_row_from, header_row_to=right_table__header_row_to)
        st.dataframe(right_df)

st.header('02 Set Join Condition')
if left_table_file is None or right_table_file is None:
    st.info('Please upload table files first.')
    st.stop()
else:
    left_join_column, right_join_column = st.columns(2)
    with left_join_column:
        left_join_column_name = st.selectbox(label='Left Join Column', options=left_df.columns)
    with right_join_column:
        right_join_column_name = st.selectbox(label='Right Join Column', options=right_df.columns)
join_mode = st.selectbox(label='Join Mode', options=['Left', 'Right', 'Inner', 'Outer', 'Cross'])


st.header('03 Download Join Result')
left_df[left_join_column_name] = left_df[left_join_column_name].astype(str)
right_df[right_join_column_name] = right_df[right_join_column_name].astype(str)
join_df = pd.merge(left=left_df, right=right_df,
                   how=join_mode.lower(),
                   left_on=left_join_column_name, right_on=right_join_column_name,
                   suffixes=('_left', '_right'))
st.dataframe(join_df)

csv = join_df.to_csv(index=False).encode('utf-8')
st.download_button(label='Download CSV', data=csv, file_name='join.csv', mime='text/csv', key='download_csv', use_container_width=True)