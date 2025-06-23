import streamlit as st

# Main page content
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

doe_type = st.radio("Select DOE type", 
                 ["Full Factorial Design(General)", "Full Factorial Design(2-Level)",
                  "Fractional Factorial Design", "Plackett-Burman Design",
                  "Box-Behnken Design", "Central Composite Design", "Mixture Design "],
                 index=0)




st.write("You selected:", doe_type)