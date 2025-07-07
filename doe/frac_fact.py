
import streamlit as st
import pandas as pd
from pyDOE3 import ff2n, fracfact
import numpy as np

options = {1:"🟩 2 Factors | 4 runs | Resolution Full",
           2:"🟥 3 Factors | 4 runs | Resolution III",
           3:"🟩 3 Factors | 8 runs | Resolution Full",
           4:"🟨 4 Factors | 8 runs | Resolution IV",
           5:"🟩 4 Factors | 16 runs | Resolution Full",
           6:"🟥 5 Factors | 8 runs | Resolution III",
           7:"🟩 5 Factors | 16 runs | Resolution V",
           8:"🟩 5 Factors | 32 runs | Resolution Full",
           9:"🟥 6 Factors | 8 runs | Resolution III",
           10:"🟨 6 Factors | 16 runs | Resolution IV",
           11:"🟩 6 Factors | 32 runs | Resolution VI",
           12:"🟩 6 Factors | 64 runs | Resolution Full",
           13:"🟥 7 Factors | 8 runs | Resolution III",
           14:"🟨 7 Factors | 16 runs | Resolution IV",
           15:"🟨 7 Factors | 32 runs | Resolution IV",
           16:"🟩 7 Factors | 64 runs | Resolution VII",
           17:"🟨 8 Factors | 16 runs | Resolution IV",
           18:"🟨 8 Factors | 32 runs | Resolution IV",
           19:"🟩 8 Factors | 64 runs | Resolution V",
           20:"🟥 9 Factors | 16 runs | Resolution III",
           21:"🟨 9 Factors | 32 runs | Resolution IV",
           22:"🟨 9 Factors | 64 runs | Resolution IV",
           23:"🟥 10 Factors | 16 runs | Resolution III",
           24:"🟨 10 Factors | 32 runs | Resolution IV",
           25:"🟨 10 Factors | 64 runs | Resolution IV",
           26:"🟥 11 Factors | 16 runs | Resolution III",
           27:"🟨 11 Factors | 32 runs | Resolution IV",
           28:"🟨 11 Factors | 64 runs | Resolution IV",
           29:"🟥 12 Factors | 16 runs | Resolution III",
           30:"🟨 12 Factors | 32 runs | Resolution IV",
           31:"🟨 12 Factors | 64 runs | Resolution IV",}

generator = {
    2:["C=AB", "a b ab"],
    4:["D=ABC", "a b c abc"],
    6:["D=AB, E=AC", "a b c ab ac"],
    7:["E=ABCD", "a b c d abcd"],
    9:["D=AB, E=AC, F=BC", "a b c ab ac bc"],
    10:["E=AB, F=AC", "a b c d ab ac"],
    11:["F=ABCDE", "a b c d e abcde"],
    13:["D=AB, E=AC, F=BC, G=ABC", "a b c ab ac bc abc"],
    14:["E=AB, F=AC, G=AD", "a b c d ab ac ad"],
    15:["F=AB, G=AC", "a b c d e ab ac"],
    16:["G=ABCDEF", "a b c d e f abcdef"],
    17:["E=AB, F=AC, G=AD, H=BC", "a b c d ab ac ad bc"],
    18:["F=AB, G=AC, H=AD", "a b c d e ab ac ad"],
    19:["G=AB, H=AC", "a b c d e f ab ac"],
    20:["E=AB, F=AC, G=AD, H=BC, I=BD", "a b c d ab ac ad bc bd",],
    21:["F=AB, G=AC, H=AD, I=AE", "a b c d e ab ac ad ae"],
    22:["G=AB, H=AC, I=AD", "a b c d e f ab ac ad"],
    23:["E=AB, F=AC, G=AD, H=BC, I=BD, J=CD", "a b c d ab ac ad bc bd cd"],
    24:["F=AB, G=AC, H=AD, I=AE, J=BC", "a b c d e ab ac ad ae bc"],
    25:["G=AB, H=AC, I=AD, J=AE", "a b c d e f ab ac ad ae"],
    26:["E=AB, F=AC, G=AD, H=BC, I=BD, J=CD, K=ABC", "a b c d ab ac ad bc bd cd abc"],
    27:["F=AB, G=AC, H=AD, I=AE, J=BC, K=BD", "a b c d e ab ac ad ae bc bd"],
    28:["G=AB, H=AC, I=AD, J=AE, K=AF", "a b c d e f ab ac ad ae af"],
    29:["E=AB, F=AC, G=AD, H=BC, I=BD, J=CD, K=ABC, L=ABD", "a b c d ab ac ad bc bd cd abc abd"],
    30:["F=AB, G=AC, H=AD, I=AE, J=BC, K=BD, L=BE", "a b c d e ab ac ad ae bc bd be"],
    31:["G=AB, H=AC, I=AD, J=AE, K=AF, L=BC", "a b c d e f ab ac ad ae af bc"]
}



def render():

    num_runs_resolution = st.selectbox(
        "Select Number of Factors and Runs",
        options=list(options.keys()),
        format_func=lambda x: options[x]
    )
    st.markdown(f"**Selected Design:** {num_runs_resolution}")
    col1, col2 = st.columns(2)

    with col1:
        num_center_point = st.number_input("No. of Center Points:", min_value=0, step=1)
    with col2:
        num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)

    num_factors = int(options[num_runs_resolution].split()[1])
    ff_df = pd.DataFrame({
        "Factor": [f'Factor {i+1}' for i in range(num_factors)],
        "Low": [-1.0] * num_factors,
        "High": [1.0] * num_factors,})
    
    ff_editor = st.data_editor(ff_df, hide_index=True)

    if st.button("Generate Factorial Design"):
        if num_runs_resolution in generator:
            coded_design = fracfact(generator[num_runs_resolution][1])
            
        else:
            coded_design = ff2n(num_factors)


        coded = {-1: "Low", 1: "High"}
        mapped_design = np.empty_like(coded_design, dtype=object)

        for col_idx in range(num_factors):
            mapped_design[:, col_idx] = [ff_editor.loc[col_idx,coded[code]] for code in coded_design[:, col_idx]]

        mapped_df = pd.DataFrame(mapped_design, columns=ff_editor["Factor"].tolist())

        for i in range(num_replicates-1):
            mapped_df = pd.concat([mapped_df, mapped_df.copy()], ignore_index=True)

        for j in range(num_center_point):
            new_row = [
                        (ff_editor.loc[k, "Low"] + ff_editor.loc[k, "High"]) / 2
                        for k in range(num_factors)
                    ]
            mapped_df = pd.concat([mapped_df, pd.DataFrame([new_row], columns=ff_editor["Factor"].tolist())], ignore_index=True)

        st.dataframe(mapped_df)


