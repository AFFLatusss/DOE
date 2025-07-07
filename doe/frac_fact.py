
import streamlit as st
import pandas as pd

options = {1:"2 Factors | 4 runs | Resolution Full",
           2:"3 Factors | 4 runs | Resolution III",
           3:"3 Factors | 8 runs | Resolution Full",
           4:"4 Factors | 8 runs | Resolution IV",
           5:"4 Factors | 16 runs | Resolution Full",
           6:"5 Factors | 8 runs | Resolution III",
           7:"5 Factors | 16 runs | Resolution V",
           8:"5 Factors | 32 runs | Resolution Full",
           9:"6 Factors | 8 runs | Resolution III",
           10:"6 Factors | 16 runs | Resolution IV",
           11:"6 Factors | 32 runs | Resolution VI",
           12:"6 Factors | 64 runs | Resolution Full",
           13:"7 Factors | 8 runs | Resolution III",
           14:"7 Factors | 16 runs | Resolution IV",
           15:"7 Factors | 32 runs | Resolution IV",
           16:"7 Factors | 64 runs | Resolution VII",
           17:"8 Factors | 16 runs | Resolution IV",
           18:"8 Factors | 32 runs | Resolution IV",
           19:"8 Factors | 64 runs | Resolution V",
           20:"9 Factors | 16 runs | Resolution III",
           21:"9 Factors | 32 runs | Resolution IV",
           22:"9 Factors | 64 runs | Resolution IV",
           23:"10 Factors | 16 runs | Resolution III",
           24:"10 Factors | 32 runs | Resolution IV",
           25:"10 Factors | 64 runs | Resolution IV",
           26:"11 Factors | 16 runs | Resolution III",
           27:"11 Factors | 32 runs | Resolution IV",
           28:"11 Factors | 64 runs | Resolution IV",
           29:"12 Factors | 16 runs | Resolution III",
           30:"12 Factors | 32 runs | Resolution IV",
           31:"12 Factors | 64 runs | Resolution IV",}

generator = {
    2:"C=AB",
    4:"D=ABC",
    6:"D=AB, E=AC",
    7:"E=ABCD",
    9:"D=AB, E=AC, F=BC",
    10:"E=AB, F=AC",
    11:"F=ABCDE",
    13:"D=AB, E=AC, F=BC, G=ABC",
    14:"E=AB, F=AC, G=AD",
    15:"F=AB, G=AC",
    16:"G=ABCDEF",
    17:"E=AB, F=AC, G=AD, H=BC",
    18:"F=AB, G=AC, H=AD",
    19:"G=AB, H=AC",
    17:"E=AB, F=AC, G=AD, H=BC, I=BD",
    18:"F=AB, G=AC, H=AD, I=AE",
    19:"G=AB, H=AC, I=AD",
    20:"E=AB, F=AC, G=AD, H=BC, I=BD",
    21:"F=AB, G=AC, H=AD, I=AE",
    22:"G=AB, H=AC, I=AD",
    23:"E=AB, F=AC, G=AD, H=BC, I=BD, J=CD",
    24:"F=AB, G=AC, H=AD, I=AE, J=BC",
    25:"G=AB, H=AC, I=AD, J=AE",
    26:"E=AB, F=AC, G=AD, H=BC, I=BD, J=CD, K=ABC",
    27:"F=AB, G=AC, H=AD, I=AE, J=BC, K=BD",
    28:"G=AB, H=AC, I=AD, J=AE, K=AF",
    29:"E=AB, F=AC, G=AD, H=BC, I=BD, J=CD, K=ABC, L=ABD",
    30:"F=AB, G=AC, H=AD, I=AE, J=BC, K=BD, L=BE",
    31:"G=AB, H=AC, I=AD, J=AE, K=AF, L=BC"
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

    num_factors = int(options[num_runs_resolution].split()[0])
    ff_df = pd.DataFrame({
        "Factor": [f'Factor {i+1}' for i in range(num_factors)],
        "Low": [-1] * num_factors,
        "High": [1] * num_factors,})
    
    ff_editor = st.data_editor(ff_df)

    if st.button("Generate Factorial Design"):
        pass