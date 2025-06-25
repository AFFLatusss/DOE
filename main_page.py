import streamlit as st
import pandas as pd
from streamlit import column_config
from pyDOE2 import *

# Main page content
st.markdown("# Design of Experiment(DOE) 🎈")
st.sidebar.markdown("# Design of Experiment 🎈")

doe_type = st.radio("Select DOE type", 
                 ["Full Factorial Design(General)",
                  "Fractional Factorial Design", "Plackett-Burman Design",
                  "Box-Behnken Design", "Central Composite Design", "Mixture Design "],
                 index=0)




st.write("You selected:", doe_type)

# Display additional information based on the selected DOE type
match doe_type:
    case "Full Factorial Design(General)":


        col1, col2, col3 = st.columns(3)

        with col1:
            num_factor = st.number_input("NO. of Factors", min_value=2, step=1)
        with col2:
            num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)
        with col3:
            num_blocks = st.number_input("NO. of Blocks", min_value=1, step=1)
        # title = st.text_input("Level Values(Separated by comma ',')", "-1,1")
        # st.write("The current movie title is", title)

        # n_factors = int(edited_df["NO. of Factors:"].iloc[0])
        default_levels = [2] * num_factor
        default_level_values = [[i for i in range(lvl)] for lvl in default_levels]

        ff_df = pd.DataFrame({
            "Factor": [f'Factor {i+1}' for i in range(num_factor)],
            "Levels": default_levels,
            "Level Values": [",".join(map(str, range(lvl))) for lvl in default_levels]
        })

        ff_editor = st.data_editor(ff_df,column_config={
                    "Levels": column_config.NumberColumn(
                        "Levels",
                        help="Must be at least 2",
                        min_value=2,
                        step=1
                    )
                },
                use_container_width=True
            )

        # check if the user has provided valid levels
        for i in range(len(ff_editor)):
            if len(ff_editor.loc[i, "Level Values"].split(",")) != ff_editor.loc[i, "Levels"]:
                st.error(f"Number of level values for Factor {i+1} does not match the number of levels. Please correct it.")
                break

        if st.button("Generate Factorial Design"):
        # Generate the full factorial design
            Levels = ff_editor["Levels"].tolist()
            Level_values = [val.split(',') for val in ff_editor["Level Values"].tolist()]


            print(Level_values)
            coded_design = fullfact(Levels)

            mapped_design = np.empty_like(coded_design, dtype=object)

            for col_idx, levels in enumerate(Level_values):
                mapped_design[:, col_idx] = [levels[int(code)] for code in coded_design[:, col_idx]]

            mapped_df = pd.DataFrame(mapped_design, columns=ff_editor["Factor"].tolist())

            for i in range(num_replicates -1):
                mapped_df = pd.concat([mapped_df, mapped_df.copy()], ignore_index=True)

            final_df = st.dataframe(mapped_df)




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


