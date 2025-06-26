import streamlit as st
import pandas as pd


st.markdown("# DOE Analyse")
# data = st.file_uploader("Upload a CSV file", type=["csv"])

st.set_page_config(page_title="DOE Analyse", layout="wide")

st.sidebar.header("🛠 Setup")

# Option to upload CSV
st.sidebar.subheader("Upload Factor Data (optional)")
data = st.sidebar.file_uploader("Choose a CSV file", type="csv")

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
else:
    st.info("No CSV uploaded. Please upload a CSV to proceed. Format: one column per factor, no response column.")