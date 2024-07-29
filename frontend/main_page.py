import streamlit as st


def handle_logout():
    if 'jwt_token' in st.session_state:
        del st.session_state['jwt_token']
    st.rerun()


pages = {
    "Person": [
        st.Page("Person/get_persons.py", title="Person List"),
        st.Page("Person/obtain_person.py", title="Get Person"),
        st.Page("Person/create_person.py", title="Create Person"),
        st.Page("Person/update_person.py", title="Update Person"),
        st.Page("Person/delete_person.py", title="Delete Person"),
    ],
    "Vehicle": [
        st.Page("Vehicle/get_vehicles.py", title="Vehicles List"),
        st.Page("Vehicle/obtain_vehicle.py", title="Get Vehicle"),
        st.Page("Vehicle/create_vehicle.py", title="Create Vehicle"),
        st.Page("Vehicle/update_vehicle.py", title="Update Vehicle"),
        st.Page("Vehicle/delete_vehicle.py", title="Delete Vehicle"),
    ],
    "Officer": [
        st.Page("Officer/get_officers.py", title="Officers List"),
        st.Page("Officer/obtain_officer.py", title="Get Officer"),
        st.Page("Officer/create_officer.py", title="Create Officer"),
        st.Page("Officer/update_officer.py", title="Update Officer"),
        st.Page("Officer/delete_officer.py", title="Delete Officer"),
    ]
}


def main_page():
    st.sidebar.title("Menu")
    if st.sidebar.button("Logout"):
        handle_logout()
    pg = st.navigation(pages)
    pg.run()
