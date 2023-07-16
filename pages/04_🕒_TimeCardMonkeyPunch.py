import streamlit as st
import pandas as pd
import datetime
import extra_streamlit_components as stx
from page_utility.time_card_monkey_punch__func import apollo_hr_shiftschedule_text_to_dataframe
from page_utility.time_card_monkey_punch__func import apollo_hr_leave_list_text_to_dataframe
from page_utility.time_card_monkey_punch__func import apollo_hr_shiftschedule_df_to_punch_action
from page_utility.time_card_monkey_punch__func import apollo_hr_leave_list_df_to_punch_action
from page_utility.time_card_monkey_punch__func import apollo_hr_shiftschedule_punch_action_to_break_punch_action
from page_utility.time_card_monkey_punch__func import apollo_hr_punch_action_to_punch_log
import io

# ==============================================
# 設定 Page Config
# ==============================================
st.set_page_config(page_title='OfficeMonkeyRun : TimeCardMonkeyPunch',
                   page_icon=':monkey_face:',
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

# ==============================================
# 設定 Cookie 管理機制
# ==============================================
cookie_manager = stx.CookieManager()
cookie_expires_at = datetime.datetime.now() + datetime.timedelta(days=365)

# ==============================================
# Page Title
# ==============================================
st.title('TimeCardMonkeyPunch')


# ==============================================
# Basic Info
# ==============================================
st.header('1.Basic Info')
month_list__start = (pd.Timestamp.now(tz='Asia/Taipei') - pd.DateOffset(months=13)).strftime('%Y-%m')
month_list__end = (pd.Timestamp.now(tz='Asia/Taipei') - pd.DateOffset(months=0)).strftime('%Y-%m')

month_list = pd.date_range(start=month_list__start, end=month_list__end, freq='MS').strftime('%Y-%m').tolist()
month_list.reverse()

month = st.selectbox(label='Month', options=month_list, index=1, key='month')


def write_cookie():
    cookie_manager.set(cookie='employee_no', val=st.session_state.get('employee_no'), expires_at=cookie_expires_at, key='cookie__employee_no')
    cookie_manager.set(cookie='employee_name', val=st.session_state.get('employee_name'), expires_at=cookie_expires_at, key='cookie__employee_name')
    cookie_manager.set(cookie='location', val=st.session_state.get('location'), expires_at=cookie_expires_at, key='cookie__location')


employee_column, name_column, location_column = st.columns(3)
with employee_column:
    employee_no__in_cookie = cookie_manager.get(cookie='employee_no')
    employee_no__default = employee_no__in_cookie if employee_no__in_cookie != 'None' else ''
    employee_no = st.text_input(label='Employee Number', value=employee_no__default, placeholder='員工編號', key='employee_no', on_change=write_cookie)
with name_column:
    employee_name__in_cookie = cookie_manager.get(cookie='employee_name')
    employee_name__default = employee_name__in_cookie if employee_name__in_cookie != 'None' else ''
    employee_name = st.text_input(label='Employee Name', value=employee_name__default, placeholder='員工姓名',  key='employee_name', on_change=write_cookie)
with location_column:
    location__in_cookie = cookie_manager.get(cookie='location')
    location__default = location__in_cookie if location__in_cookie != 'None' else ''
    location = st.text_input(label='Location', value=location__default, placeholder='工作地點',  key='location', on_change=write_cookie)


# ==============================================
# Schedule & Dayoff INPUT
# ==============================================
schedule_column, leave_column = st.columns(2)

with schedule_column:
    st.header('2.Schedule')
    shift_schedule = st.text_area(label='Shift Schedule',
                                  key='shift_schedule',
                                  value='',
                                  height=120)
    shift_schedule_df = apollo_hr_shiftschedule_text_to_dataframe(shift_schedule=shift_schedule)
    st.dataframe(shift_schedule_df, height=240, use_container_width=True)

with leave_column:
    st.header('3.Leave List')
    leave_list = st.text_area(label='Leave List',
                              key='leave_list',
                              value='',
                              height=120)
    leave_list_df = apollo_hr_leave_list_text_to_dataframe(leave_list=leave_list)
    st.dataframe(leave_list_df, height=240, use_container_width=True)

# ==============================================
# Combine Schedule & Dayoff
# ==============================================
st.header('4.Punch Record')

# ==============================================
# Processing...
# ==============================================

if shift_schedule_df.empty:
    st.stop()

last_day_in_month = pd.Timestamp(month).to_period('M').to_timestamp(freq='M', how='S')
if shift_schedule_df['day'].max() != last_day_in_month.day:
    st.warning(f'輸入的 Shift Schedule 日期不符合設定月份的天數，請確認是否正確')

with st.expander(label='Generator', expanded=False):
    st.caption('Shift Schedule -> Shift Schedule Punch Action')
    shift_schedule__punch_action_df, shift_schedule__debug_df = apollo_hr_shiftschedule_df_to_punch_action(shift_schedule_df=shift_schedule_df, month=month)
    st.dataframe(shift_schedule__debug_df, height=240, use_container_width=True)

    st.caption('Leave List -> Leave Punch Action')
    leave_list__punch_action_df, leave_list__debug_df = apollo_hr_leave_list_df_to_punch_action(leave_list_df=leave_list_df)
    st.dataframe(leave_list__debug_df, height=240, use_container_width=True)

    st.caption('Shift Schedule Punch Action -> Break Punch Action')
    break__punch_action_df, break__debug_df = apollo_hr_shiftschedule_punch_action_to_break_punch_action(
        shift_schedule__punch_action_df=shift_schedule__punch_action_df)
    st.dataframe(break__debug_df, height=240, use_container_width=True)

    punch_log_df, punch_action_df = apollo_hr_punch_action_to_punch_log(
        punch_action_df_list=[shift_schedule__punch_action_df, leave_list__punch_action_df, break__punch_action_df],
        month=month,
        employee_no=employee_no,
        employee_name=employee_name,
        location=location)
    st.dataframe(punch_action_df, height=240, use_container_width=True)

st.dataframe(punch_log_df, height=240, use_container_width=True)

# REF : https://stackoverflow.com/questions/75323732/how-to-download-streamlit-output-data-frame-as-excel-file
# REF https://stackoverflow.com/questions/76090979/xlsxwriter-object-has-no-attribute-save-did-you-mean-save
buffer = io.BytesIO()
writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
# Write each dataframe to a different worksheet.
punch_log_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
download2 = st.download_button(
    label="Download data as Excel",
    data=buffer,
    file_name=f'{month}月打卡紀錄.xlsx',
    mime='application/vnd.ms-excel',
    use_container_width=True
)
