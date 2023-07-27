import streamlit as st
import pandas as pd
from page_utility import read_table_file_to_df
import io


# ==============================================
# 設定 Page Config
# ==============================================
st.set_page_config(page_title='OfficeMonkeyRun : MultiMonkeyFileConcat',
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
st.title('MultiMonkeyFileConcat')


# ==============================================
# Upload File
# ==============================================
st.header('1. Upload Table Files')
uploaded_table_file = st.file_uploader(
    label='Left Table', type=['csv', 'xlsx'], key='duplicated_drop_file', accept_multiple_files=True)

if uploaded_table_file is not None and len(uploaded_table_file) > 0:
    file_df__list = []
    for file in uploaded_table_file:
        file_df = read_table_file(table_file=file)
        file_df__list.append(file_df)

    concat_df = pd.concat(file_df__list, axis=0, ignore_index=True)
else:
    concat_df = pd.DataFrame()


# ==============================================
# Download File
# ==============================================
st.header('2. Download Concatenated Files')
if uploaded_table_file is None:
    st.info('Please upload table files first.')
    st.stop()
else:
    st.dataframe(concat_df, use_container_width=True)
    # Download CSV
    csv = concat_df.to_csv(index=False).encode('utf-8')
    filename = f'GroupBy_Agg.csv'
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name=filename,
        mime='text/csv',
        key='download_csv',
        use_container_width=True)

    # Download Excel
    # REF : https://stackoverflow.com/questions/75323732/how-to-download-streamlit-output-data-frame-as-excel-file
    # REF https://stackoverflow.com/questions/76090979/xlsxwriter-object-has-no-attribute-save-did-you-mean-save
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    concat_df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    download = st.download_button(
        label="DOWNLOAD CONCATENATED EXCEL FILE",
        data=buffer,
        file_name=f'Concatenated.xlsx',
        mime='application/vnd.ms-excel',
        use_container_width=True
    )
