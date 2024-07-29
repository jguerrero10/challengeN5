import streamlit as st

from utils.services import get_entity

st.title("Get Officer")

with st.form("get_officer"):
    st.write("Form to obtain a Officer")
    number_identifier = st.text_input("Number Identifier")
    submit = st.form_submit_button('Send')

if submit:
    officer = get_entity("officer", number_identifier, st.session_state['jwt_token'])
    if officer.get("success"):
        st.success("Person successfully obtained")
        st.write(officer.get("message"))
    else:
        st.error("Person could not be obtained")
        st.write(officer.get("message"))
