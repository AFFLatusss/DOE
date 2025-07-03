"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np



# Define the pages
doe_page = st.Page("DoE.py", title="DoE", icon="🎈")
analyse_page = st.Page("DoE_A.py", title="DoE Analyse", icon="❄️")
# page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")
# factorial_design = st.Page("factorial_design.py", title="Factorial Design", icon="🎉")
# Set up navigation
pg = st.navigation([doe_page, analyse_page])

# Run the selected page
pg.run()