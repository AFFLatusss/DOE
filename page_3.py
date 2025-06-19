import streamlit as st
import pandas as pd
from pyDOE2 import fullfact
from statsmodels.formula.api import ols

st.set_page_config(page_title="DOE Tool with CSV Support", layout="wide")
st.title("📊 Design of Experiments (DOE) Web App")

st.sidebar.header("🛠 Experiment Setup")

# Option to upload CSV
st.sidebar.subheader("Upload Factor Data (optional)")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📂 Uploaded Factor Data")
    st.dataframe(df)
    if df.shape[1] < 2:
        st.warning("Please upload a CSV with at least two columns for factors.")
    else:
        factor_names = df.columns.tolist()
        num_factors = len(factor_names)
        levels = [2] * num_factors
        design = fullfact(levels)
        design_df = pd.DataFrame(design, columns=factor_names)
        design_df = design_df * 2 - 1  # Convert to -1/+1
        st.subheader("🧪 Generated Design Matrix")
        st.dataframe(design_df)

        st.subheader("📝 Enter Response Values")
        responses = []
        for i in range(len(design_df)):
            val = st.number_input(f"Response for Run {i+1}: {design_df.iloc[i].values}", key=f"resp_{i}")
            responses.append(val)

        if any(responses):
            design_df["Response"] = responses
            formula = "Response ~ " + " + ".join([f"Q('{name}')" for name in factor_names])
            model = ols(formula, data=design_df).fit()
            st.subheader("📈 Regression Summary")
            st.text(model.summary())
else:
    st.info("No CSV uploaded. Please upload a CSV to proceed. Format: one column per factor, no response column.")
