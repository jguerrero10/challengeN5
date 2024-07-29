import streamlit as st
from utils.auth import login


def handle_login(username, password):
    token = login(username, password)
    login_success = token.get("success", None)
    if login_success:
        st.session_state['jwt_token'] = token.get("token", None)
        st.rerun()
    else:
        st.error(token.get("message", "Invalid credentials"))


def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        handle_login(username, password)
