
import streamlit as st
import pandas as pd
import itertools
import numpy as np

def render():

    design_type = st.selectbox("Design Type", ["Simplex-Centroid", "Simplex-Lattice"])
    
    num_components = st.slider("Number of Components", min_value=2, max_value=4)

    if design_type == "Simplex-Lattice":
        m = st.slider("Lattice Degree (m)", min_value=2, max_value=5)
    else:
        m = None  # Not needed for centroid

    component_names = [f"Comp_{i+1}" for i in range(num_components)]

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
    if design_type == "Simplex-Centroid":
        design_df = generate_centroid_design(num_components)
    elif design_type == "Simplex-Lattice":
        design_df = generate_lattice_design(num_components, m)

    st.subheader("📋 Design Points")
    st.dataframe(design_df)

