
import streamlit as st
import pandas as pd
import itertools
import numpy as np
from pypoman import compute_polytope_vertices


    # -----------------------
    # Simplex-Centroid Design
    # -----------------------
def generate_simplex_centroid(k):
    all_points = []

    # Loop from 1 component up to k components at a time
    for i in range(1, k + 1):
        for combo in itertools.combinations(range(k), i):
            point = [0.0] * k
            for j in combo:
                point[j] = 1.0 / i
            all_points.append(point)

    return all_points

def generate_simplex_lattice(k, m):

    levels = [i / m for i in range(m + 1)]  # Discrete steps from 0 to 1
    grid = list(itertools.product(levels, repeat=k))  # All combinations
    valid_points = [pt for pt in grid if abs(sum(pt) - 1.0) < 1e-6]  # Keep only those summing to 1
    return valid_points

def extreme_vertices_design(mins, maxs):
    """
    Compute the exact extreme vertices (corner points) of a mixture region defined by:
      L_i ≤ x_i ≤ U_i  for i=1..k
      sum(x_i) = 1

    Returns a DataFrame of all extreme vertices.
    """
    print(mins, maxs)
    mins = np.asarray(mins, dtype=float)
    maxs = np.asarray(maxs, dtype=float)
    k = len(mins)
    assert len(maxs) == k, "mins and maxs must have same length"

    # Build inequality system A x <= b
    # 1) Bounds: x_i <= U_i     →  A row: e_i,   b: U_i
    #            -x_i <= -L_i    →  A row: -e_i,  b: -L_i
    # 2) Sum constraint: sum x_i <= 1
    #            -sum x_i <= -1
    A = []
    b = []

    # bounds
    for i in range(k):
        e = np.zeros(k)
        e[i] = 1.0
        A.append(e.copy());    b.append(maxs[i])
        A.append(-e.copy());   b.append(-mins[i])

    # mixture sum == 1
    A.append(np.ones(k));  b.append(1.0)
    A.append(-np.ones(k)); b.append(-1.0)

    # enumerate vertices
    verts = compute_polytope_vertices(np.array(A), np.array(b))

    # round small numerical noise
    verts = np.unique(np.round(verts, 8), axis=0)
    print("in function")
    return pd.DataFrame(verts, columns=[f"x{i+1}" for i in range(k)])


def render():

    # design_type = st.selectbox("Design Type", ["Simplex-Centroid", "Simplex-Lattice"])
    options = ["Simplex-Centroid", "Simplex-Lattice", "Extreme-Vertices"]
    selection = st.pills("Design Type", options, selection_mode="single")
    st.markdown(f"Your selected options: {selection}.")

    if selection:
        selected = selection

        # Determine how many columns you want based on the selected design
        num_cols = 5 if selected == "Simplex-Lattice" else 4

        # Dynamically create the columns
        cols = st.columns(num_cols)

        with cols[0]:
            num_factor = st.number_input("NO. of Factors", min_value=2, step=1)
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
            "Lower Bounds": [0.0] * num_factor,
            "High Bounds": [1.0] * num_factor,
            })
    
        ff_editor = st.data_editor(ff_df, hide_index=True)

      
        # -----------------------
        # Generate Design
        # -----------------------
        if st.button("Generate Design"):
            if selected == "Simplex-Centroid":
                coded_design = generate_simplex_centroid(num_factor)
            elif selected == "Simplex-Lattice":
                coded_design = generate_simplex_lattice(num_factor, lattice_degree)
            elif selected == "Extreme-Vertices":
                mins = ff_editor["Lower Bounds"].tolist()
                maxs = ff_editor["High Bounds"].tolist()
                coded_design = extreme_vertices_design(mins, maxs)
            st.subheader("📋 Design Points")
            
            if num_replicates > 1:
                coded_design = pd.concat([coded_design] * num_replicates, ignore_index=True)
                
            st.dataframe(coded_design)

