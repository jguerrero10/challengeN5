import streamlit as st

from utils.services import create_entity

st.title("Create Officer")

with st.form("create_officer"):
    st.write("Form to register a Officer")
    name = st.text_input("Name")
    number_identifier = st.text_input("Number Identifier")
    username = st.text_input("Username")
    password = st.text_input("Password")
    submit = st.form_submit_button('Send')

if submit:
    data = {
        "name": name,
        "number_identifier": number_identifier,
        "username": username,
        "password": password
    }
    officer_created = create_entity("officer", data, st.session_state['jwt_token'])
    if officer_created.get("success"):
        st.success("Officer has been created")
        st.write(officer_created.get("message"))
    else:
        st.error("Officer could not be created")
        st.write(officer_created.get("message"))
