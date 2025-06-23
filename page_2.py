import streamlit as st
import pandas as pd


st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

data = st.file_uploader("Upload a CSV file", type=["csv"])

if data:
    df = pd.read_csv(data)
    st.dataframe(df)

    columns = df.columns.tolist() if data else []
    factors = st.multiselect(
        "Select Factors?",
        columns,
        default=[],
    )

    # st.write("You selected:", factors)

    st.selectbox('Select a response variable', options=[x for x in columns if x not in factors], index=0)