import numpy as np
import streamlit as st
import pandas as pd
from streamlit import column_config
from pyDOE3 import *

def render():
    col1, col2, col3 = st.columns(3)

    with col1:
        num_factor = st.number_input("NO. of Factors", min_value=3, step=1)
    with col2:
        num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)
    with col3:
        num_center_point = st.number_input("NO. of Center Point", min_value=1, step=1)

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
        coded_design = bbdesign(num_factor, num_center_point)
        print(coded_design)
        # coded = {-1: "Low", 1: "High"}


        mapped_design = np.empty_like(coded_design, dtype=object)

        for col_idx in range(num_factor):
            low = ff_editor.loc[col_idx, "Low"]
            high = ff_editor.loc[col_idx, "High"]
            center = (low + high) / 2

            for row_idx, code in enumerate(coded_design[:, col_idx]):
                if code == -1:
                    mapped_design[row_idx, col_idx] = low
                elif code == 1:
                    mapped_design[row_idx, col_idx] = high
                else:  # center point
                    mapped_design[row_idx, col_idx] = center




        mapped_df = pd.DataFrame(mapped_design, columns=ff_editor["Factor"].tolist())


        if num_replicates > 1:
            mapped_df = pd.concat([mapped_df] * num_replicates, ignore_index=True)


        st.dataframe(mapped_df)