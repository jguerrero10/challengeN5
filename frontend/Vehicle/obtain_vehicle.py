import streamlit as st

from utils.services import get_entity

st.title("Get Vehicle by Id")

with st.form("get_vehicle"):
    st.write("Form to obtain a Vehicle")
    email = st.text_input("Person Email")
    patent_plate = st.text_input("Patent Plate")
    submit = st.form_submit_button('Send')

if submit:
    person = get_entity("vehicle", patent_plate, st.session_state['jwt_token'], params={'person_email': email})
    if person.get("success"):
        st.success("Vehicle has been successfully obtained")
        st.write(person.get("message"))
    else:
        st.error("Vehicle could not be obtained")
        st.write(person.get("message"))
