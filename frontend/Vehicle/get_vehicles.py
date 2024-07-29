import pandas as pd
import streamlit as st

from utils.services import list_entities

st.title("List of vehicles")

with st.form("get_vehicle"):
    st.write("Form to obtain vehicles of a Person")
    email = st.text_input("Person Email")
    submit = st.form_submit_button('Send')

entities = list_entities("vehicle", st.session_state['jwt_token'], params={'person_email': email})
df = pd.DataFrame(entities)
st.table(df)
