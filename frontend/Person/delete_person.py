import streamlit as st

from utils.services import delete_entity

st.title("Delete Person by Id")

with st.form("delete_person"):
    st.write("Form to delete a Person")
    person_id = st.text_input("Id")
    submit = st.form_submit_button('Send')

if submit:
    person = delete_entity("person", person_id, st.session_state['jwt_token'])
    if person.get("success"):
        st.success("Person has been deleted")
        st.write(person.get("message"))
    else:
        st.error("Person could not be deleted")
        st.write(person.get("message"))
