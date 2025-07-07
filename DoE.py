import streamlit as st
import pandas as pd
import doe

# Main page content
st.markdown("# Design of Experiment(DOE) 🎈")
st.sidebar.markdown("# Design of Experiment 🎈")

doe_type = st.radio("Select DOE type", 
                 ["Full Factorial Design(General)",
                  "Fractional Factorial Design", "Plackett-Burman Design",
                  "Box-Behnken Design", "Central Composite Design", "Mixture Design"],
                 index=0)




st.write("You selected:", doe_type)

# Display additional information based on the selected DOE type
match doe_type:
    case "Full Factorial Design(General)":
        doe.full_fact()
    case "Fractional Factorial Design":
        doe.frac_fact()
    case "Plackett-Burman Design":
        doe.plackett_burman()
    case "Box-Behnken Design":
        doe.box_behnken()
    case "Central Composite Design":
        doe.central_composite()
    case "Mixture Design":
        doe.mixture()

