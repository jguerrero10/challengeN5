import streamlit as st

from utils.services import update_entity

st.title("Update Vehicle")

with st.form("update_vehicle"):
    st.write("Form to update a Vehicle")
    email = st.text_input("Person Email")
    patent_plate = st.text_input("Patent Plate")
    brand = st.text_input("brand")
    color = st.text_input("color")
    submit = st.form_submit_button('Send')

if submit:
    vehicle_updated = update_entity(
        "vehicle",
        patent_plate,
        st.session_state['jwt_token'],
        {
            "brand": brand,
            "color": color,
            "patent_plate": patent_plate
        },
        params={
            "person_email": email
        },
        method="put"
    )
    if vehicle_updated.get("success"):
        st.success("Vehicle is Updated")
        st.write(vehicle_updated.get("message"))
    else:
        st.error("Vehicle is not Updated")
        st.write(vehicle_updated.get("message"))
