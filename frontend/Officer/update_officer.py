import streamlit as st

from utils.services import update_entity

st.title("Update Officer")

with st.form("update_officer"):
    st.write("Form to update a Officer")
    number_identifier = st.text_input("Number Identifier")
    name = st.text_input("Name")
    submit = st.form_submit_button('Send')

if submit:
    person_updated = update_entity(
        "officer",
        number_identifier,
        st.session_state['jwt_token'],
        {"name": name}
    )
    if person_updated.get("success"):
        st.success("Person has been updated")
        st.write(person_updated.get("message"))
    else:
        st.error("Person could not be updated")
        st.write(person_updated.get("message"))
