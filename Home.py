import streamlit as st


st.set_page_config(page_title='OfficeMonkeyRun',
                   page_icon=':monkey_face:',
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)

# ==============================================


sidebar_title = '''
    <a target="_self" href="./" style="text-decoration:none;">
        <h1 style="font-family: 'Helvetica', 'Arial', sans-serif;font-size:950%;line-height:0.8em;text-color:white;font-weight:300;text-align:left;">
            Office</br>Monkey</br>Run
        </h1>
    </a>
    <aside style="margin: 0.5em 0.25em 1em 0.75em;text-align:left;">
        Monkeys must be in office,</br> but they can be set free to run.
    </aside>
    '''
st.markdown(sidebar_title, unsafe_allow_html=True)