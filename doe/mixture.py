
import streamlit as st
import pandas as pd
import itertools
import numpy as np

def render():

    # design_type = st.selectbox("Design Type", ["Simplex-Centroid", "Simplex-Lattice"])
    options = ["Simplex-Centroid", "Simplex-Lattice", "Extreme-Vertices"]
    selection = st.pills("Design Type", options, selection_mode="single")
    st.markdown(f"Your selected options: {selection}.")

    if selection:
        selected = selection[0]

        # Determine how many columns you want based on the selected design
        num_cols = 5 if selected == "Simplex-Lattice" else 4

        # Dynamically create the columns
        cols = st.columns(num_cols)

        with cols[0]:
            num_factor = st.number_input("NO. of Factors", min_value=3, step=1)
        with cols[1]:
            num_replicates = st.number_input("NO. of Replicates", min_value=1, step=1)
        with cols[2]:
            num_center_point = st.number_input("NO. of Center Point", min_value=0, step=1)
        with cols[3]:
            total_sum = st.number_input("Total Sum", min_value=1, step=1, value=1)

        if selected == "Simplex-Lattice":
            with cols[4]:
                lattice_degree = st.number_input("Lattice Degree", min_value=1, max_value=10, step=1)

        ff_df = pd.DataFrame({
            "Factor": [f'Factor {i+1}' for i in range(num_factor)],
            "Lower Bounds": [-1] * num_factor,
            "High Bounds": [1] * num_factor,
            })



        component_names = [f"Factor {i+1}" for i in range(num_factor)]

        # -----------------------
        # Simplex-Centroid Design
        # -----------------------
        def generate_centroid_design(n):
            def compositions(n, k):
                """All compositions of n into k parts"""
                return [p for p in itertools.combinations_with_replacement(range(k), n)]

            all_points = []
            for i in range(1, n+1):
                for combo in itertools.combinations(range(n), i):
                    point = [0.0] * n
                    for j in combo:
                        point[j] = 1.0 / i
                    all_points.append(point)
            return pd.DataFrame(all_points, columns=component_names)

        # ---------------------
        # Simplex-Lattice Design
        # ---------------------
        def generate_lattice_design(n, m):
            """Generates a simplex-lattice design"""
            levels = [i/m for i in range(m+1)]
            grid = list(itertools.product(levels, repeat=n))
            grid = [pt for pt in grid if abs(sum(pt) - 1.0) < 1e-6]
            return pd.DataFrame(grid, columns=component_names)

        # -----------------------
        # Generate Design
        # -----------------------
        if selection[0] == "Simplex-Centroid":
            design_df = generate_centroid_design(num_factor)
        elif selection[0] == "Simplex-Lattice":
            design_df = generate_lattice_design(num_factor, m)

        st.subheader("📋 Design Points")
        st.dataframe(design_df)

