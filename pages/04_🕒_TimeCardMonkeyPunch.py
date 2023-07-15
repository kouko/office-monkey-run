import streamlit as st
import pandas as pd
import datetime
import extra_streamlit_components as stx
from page_utility.time_card_monkey_punch__func import apollo_hr_shiftschedule_text_to_dataframe
from page_utility.time_card_monkey_punch__func import apollo_hr_leave_list_text_to_dataframe

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
month_list__end = (pd.Timestamp.now(tz='Asia/Taipei') - pd.DateOffset(months=1)).strftime('%Y-%m')

month_list = pd.date_range(start=month_list__start, end=month_list__end, freq='MS').strftime('%Y-%m').tolist()
month_list.reverse()

month = st.selectbox(label='Month', options=month_list, index=0, key='month')


def write_cookie():
    cookie_manager.set(cookie='employee_no', val=st.session_state.get('employee_no'), expires_at=cookie_expires_at, key='cookie__employee_no')
    cookie_manager.set(cookie='employee_name', val=st.session_state.get('employee_name'), expires_at=cookie_expires_at, key='cookie__employee_name')
    cookie_manager.set(cookie='location', val=st.session_state.get('location'), expires_at=cookie_expires_at, key='cookie__location')


employee_column, name_column, location = st.columns(3)
with employee_column:
    employee_no__in_cookie = cookie_manager.get(cookie='employee_no')
    employee_no__default = employee_no__in_cookie if employee_no__in_cookie != 'None' else ''
    employee_no = st.text_input(label='Employee Number', value=employee_no__default, placeholder='員工編號', key='employee_no')
with name_column:
    employee_name__in_cookie = cookie_manager.get(cookie='employee_name')
    employee_name__default = employee_name__in_cookie if employee_name__in_cookie != 'None' else ''
    employee_name = st.text_input(label='Employee Name', value=employee_name__default, placeholder='員工姓名',  key='employee_name')
with location:
    location__in_cookie = cookie_manager.get(cookie='location')
    location__default = location__in_cookie if location__in_cookie != 'None' else ''
    location = st.text_input(label='Location', value=location__default, placeholder='工作地點',  key='location')


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
    st.dataframe(shift_schedule_df, use_container_width=True)

with leave_column:
    st.header('3.Leave List')
    leave_list = st.text_area(label='Leave List',
                              key='leave_list',
                              value='',
                              height=120)
    leave_list_df = apollo_hr_leave_list_text_to_dataframe(leave_list=leave_list)
    st.dataframe(leave_list_df, use_container_width=True)

# ==============================================
# Combine Schedule & Dayoff
# ==============================================
st.header('4.Punch Record')

