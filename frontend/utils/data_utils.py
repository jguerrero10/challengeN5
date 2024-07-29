import streamlit as st

from utils.services import create_entity


def generate_form(entity: str):
    if entity == 'person':
        name = st.text_input("Name")
        email = st.text_input("Email")
    if st.form_submit_button("Send"):
        data = {"name": name, "email": email}
        entity_created = create_entity(entity.lower(), data, st.session_state['jwt_token'])
        if entity_created:
            st.success(entity_created)
        else:
            st.error(entity_created)

