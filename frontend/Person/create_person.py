import streamlit as st

from utils.services import create_entity

st.title("Person Create")

with st.form("create_person"):
    st.write("Form to register a Person")
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit = st.form_submit_button('Send')

if submit:
    data = {"name": name, "email": email}
    person_created = create_entity("person", data, st.session_state['jwt_token'])
    if person_created.get("success"):
        st.success("Person has been created")
        st.write(person_created.get("message"))
    else:
        st.error("Person could not be created")
        st.write(person_created.get("message"))
