import streamlit as st

from utils.services import create_entity

st.title("Vehicle Create")

with st.form("create_person"):
    st.write("Form to register a Person")
    email = st.text_input("Person Email")
    brand = st.text_input("Brand")
    color = st.text_input("Color")
    patent_plate = st.text_input("Patent Plate")
    submit = st.form_submit_button('Send')

if submit:
    data = {
        "brand": brand,
        "color": color,
        "patent_plate": patent_plate,
    }
    vehicle_created = create_entity(
        "vehicle",
        data,
        st.session_state['jwt_token'],
        params={"person_email": email}
    )
    if vehicle_created.get("success"):
        st.success("Person has been created")
        st.write(vehicle_created.get("message"))
    else:
        st.error("Person could not be created")
        st.write(vehicle_created.get("message"))
