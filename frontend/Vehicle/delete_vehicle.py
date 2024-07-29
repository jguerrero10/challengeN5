import streamlit as st

from utils.services import delete_entity

st.title("Delete Vehicle")

with st.form("delete_vehicle"):
    st.write("Form to delete a Vehicle")
    email = st.text_input("Person Email")
    patent_plate = st.text_input("Patent Plate")
    submit = st.form_submit_button('Send')

if submit:
    vehicle = delete_entity(
        "vehicle",
        patent_plate,
        st.session_state['jwt_token'],
        params={'person_email': email}
    )
    if vehicle.get("success"):
        st.success("Vehicle has been deleted")
    else:
        st.error("Vehicle could not be deleted")
        st.write(vehicle.get("message"))
