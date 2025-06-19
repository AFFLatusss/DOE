"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np



# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")
factorial_design = st.Page("factorial_design.py", title="Factorial Design", icon="🎉")
# Set up navigation
pg = st.navigation([main_page, page_2, page_3, factorial_design])

# Run the selected page
pg.run()