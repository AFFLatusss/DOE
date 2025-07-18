
import streamlit as st
import pandas as pd
from streamlit import column_config
from pyDOE2 import *


def render():


    col1, col2, col3, col4= st.columns(4)

    with col1:
        num_factor = st.number_input("NO. of Factors", min_value=2, step=1)
    with col2:
        num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)
    with col3:
        num_blocks = st.number_input("NO. of Blocks", min_value=1, step=1)
    with col4:
        num_center_point = st.number_input("NO. of Center Points", min_value=0, step=1)


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
            use_container_width=True, hide_index=True
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
        # mapped_df.insert(0, "Run Order", range(1, len(mapped_df) + 1))        
        if num_replicates > 1:
            mapped_df = pd.concat([mapped_df] * num_replicates, ignore_index=True)

        for j in range(num_center_point):
            new_row = [
                        sum(map(int, Level_values[k])) / len(Level_values[k])
                        for k in range(num_factor)
                    ]
            mapped_df = pd.concat([mapped_df, pd.DataFrame([new_row], columns=ff_editor["Factor"].tolist())], ignore_index=True)

        st.dataframe(mapped_df, hide_index=True)
