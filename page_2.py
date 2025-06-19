import streamlit as st
import pandas as pd


st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

data = st.file_uploader("Upload a CSV file", type=["csv"])

if data:
    df = pd.read_csv(data)
    st.dataframe(df)
