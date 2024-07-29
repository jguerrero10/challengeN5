import streamlit as st

from utils.services import delete_entity

st.title("Delete Officer")

with st.form("delete_officer"):
    st.write("Form to delete a Officer")
    number_identifier = st.text_input("Number Identifier")
    submit = st.form_submit_button('Send')

if submit:
    officer = delete_entity("officer", number_identifier, st.session_state['jwt_token'])
    if officer.get("success"):
        st.success("Officer has been deleted")
        st.write(officer.get("message"))
    else:
        st.error("Officer could not be deleted")
        st.write(officer.get("message"))
