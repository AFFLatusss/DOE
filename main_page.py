import streamlit as st
import pandas as pd

# Main page content
st.markdown("# Design of Experiment(DOE) 🎈")
st.sidebar.markdown("# Design of Experiment 🎈")

doe_type = st.radio("Select DOE type", 
                 ["Full Factorial Design(General)", "Full Factorial Design(2-Level)",
                  "Fractional Factorial Design", "Plackett-Burman Design",
                  "Box-Behnken Design", "Central Composite Design", "Mixture Design "],
                 index=0)




st.write("You selected:", doe_type)

# Display additional information based on the selected DOE type
match doe_type:
    case "Full Factorial Design(General)":
        df = pd.DataFrame(
            [{"NO. of Factors:": 2 , "No. of Replicates:": 1, "No. of Blocks:": 1}]
        )
        edited_df = st.data_editor(df)

        if edited_df["NO. of Factors:"].iloc[0] <= 1:
            st.error("Number of factors must be at least 2.")
        if edited_df["No. of Replicates:"].iloc[0] < 1:
            st.error("Number of replicates must be at least 1.")
        if edited_df["No. of Blocks:"].iloc[0] < 1:
            st.error("Number of blocks must be at least 1.")

        title = st.text_input("Movie title", "Life of Brian")
        st.write("The current movie title is", title)







    case "Full Factorial Design(2-Level)":
        st.write("Full Factorial Design with 2 levels is a specific case where each factor has two levels (e.g., low and high).")
    case "Fractional Factorial Design":
        st.write("Fractional Factorial Design is used to reduce the number of experiments while still providing insights into the effects of factors.")
    case "Plackett-Burman Design":
        st.write("Plackett-Burman Design is a type of fractional factorial design that is particularly useful for screening experiments.")
    case "Box-Behnken Design":
        st.write("Box-Behnken Design is a response surface methodology that is used for building a second-order (quadratic) model for the response variable without needing a full three-level factorial experiment.")
    case "Central Composite Design":
        st.write("Central Composite Design is used in response surface methodology to build a second-order model for the response variable.")
    case "Mixture Design":
        st.write("Mixture Design is used when the factors are proportions of components in a mixture, and the sum of the proportions is constant.")


