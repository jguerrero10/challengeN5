import streamlit as st

from utils.services import get_entity

st.title("Get Person by Id")

with st.form("get_person"):
    st.write("Form to obtain a Person")
    person_id = st.text_input("Id")
    submit = st.form_submit_button('Send')

if submit:
    person = get_entity("person", person_id, st.session_state['jwt_token'])
    if person.get("success"):
        st.success("Person successfully obtained")
        st.write(person.get("message"))
    else:
        st.error("Person could not be obtained")
        st.write(person.get("message"))
