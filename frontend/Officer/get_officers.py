import pandas as pd
import streamlit as st

from utils.services import list_entities

st.title("List of Officers")

entities = list_entities("officer", st.session_state['jwt_token'])
df = pd.DataFrame(entities)
st.table(df)
