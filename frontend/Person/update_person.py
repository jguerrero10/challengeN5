import streamlit as st

from utils.services import update_entity

st.title("Update Person by Id")

with st.form("update_person"):
    st.write("Form to update a Person")
    person_id = st.text_input("Id")
    name = st.text_input("Name")
    submit = st.form_submit_button('Send')

if submit:
    person_updated = update_entity("person", person_id, st.session_state['jwt_token'], {"name": name})
    if person_updated.get("success"):
        st.success("Person has been updated")
        st.write(person_updated.get("message"))
    else:
        st.error("Person could not be updated")
        st.write(person_updated.get("message"))
