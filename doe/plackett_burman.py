
import streamlit as st
import pandas as pd
from streamlit import column_config
from pyDOE2 import *


def render():


    col1, col2, col3 = st.columns(3)

    with col1:
        num_factor = st.number_input("NO. of Factors", min_value=2, step=1)
    with col2:
        num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)
    with col3:
        num_center_point = st.number_input("NO. of Center Points", min_value=0, step=1)

    ff_df = pd.DataFrame({
            "Factor": [f'Factor {i+1}' for i in range(num_factor)],
            "Low": [-1]* num_factor,
            "High": [1] * num_factor,
        })
    
    ff_editor = st.data_editor(ff_df,column_config={
                "Low": column_config.NumberColumn("Low", help="Must be a number", step=1),
                "High": column_config.NumberColumn("High", help="Must be a number", step=1)
            },
            use_container_width=True, hide_index=True
        )


    if st.button("Generate Factorial Design"):
        # Validate Low < High
        for i in range(num_factor):
            if ff_editor.loc[i, "Low"] >= ff_editor.loc[i, "High"]:
                st.error(f"❌ Factor {i+1}: Low must be less than High.")
                return
            
        # Generate the pb design
        coded_design = pbdesign(num_factor)
        coded = {-1: "Low", 1: "High"}


        mapped_design = np.empty_like(coded_design, dtype=object)

        for col_idx in range(num_factor):
            mapped_design[:, col_idx] = [ff_editor.loc[col_idx,coded[code]] for code in coded_design[:, col_idx]]

        mapped_df = pd.DataFrame(mapped_design, columns=ff_editor["Factor"].tolist())


        if num_replicates > 1:
            mapped_df = pd.concat([mapped_df] * num_replicates, ignore_index=True)

        # Optionally add center points commneted for now
        # if num_center_point > 0:
        #     center_row = {
        #         factor: (ff_editor.loc[i, "Low"] + ff_editor.loc[i, "High"]) / 2
        #         for i, factor in enumerate(ff_editor["Factor"])
        #     }
        #     center_df = pd.DataFrame([center_row] * num_center_point)
        #     mapped_df = pd.concat([mapped_df, center_df], ignore_index=True)

        st.dataframe(mapped_df)
