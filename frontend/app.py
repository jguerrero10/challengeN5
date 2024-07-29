import streamlit as st
from login import login_page
from main_page import main_page


def main():
    if 'jwt_token' not in st.session_state:
        login_page()
    else:
        main_page()


if __name__ == "__main__":
    main()
