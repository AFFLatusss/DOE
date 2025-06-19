import streamlit as st
from pyDOE2 import *

st.markdown("# Factorial Design 🎉")
st.sidebar.markdown("# Factorial Design 🎉")

# Input for the number of factors
num_factors = st.number_input("Number of factors", min_value=1, max_value=10, value=2)

# Input for the number of levels 
num_levels = st.number_input("Number of levels", min_value=2, max_value=10, value=2)

# Generate the factorial design
if st.button("Generate Factorial Design"):
    if num_factors > 0 and num_levels >= 2:
        design = fullfact([num_levels, num_factors])
        st.write("Generated Factorial Design:")
        st.dataframe(design)
    else:
        st.error("Please enter valid values for factors and levels.")