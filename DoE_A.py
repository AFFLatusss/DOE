import streamlit as st
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import pingouin as pg

st.markdown("# DOE Analyse")
# data = st.file_uploader("Upload a CSV file", type=["csv"])

st.set_page_config(page_title="DOE Analyse", layout="wide")

st.sidebar.header("🛠 Setup")

# Option to upload CSV
st.sidebar.subheader("Upload Factor Data (optional)")
data = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if data:
    df = pd.read_csv(data)
    st.write("📄 Data Preview:", df.head())

    # Step 2: Let user choose response and factor columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    response_col = st.selectbox("Select Response Variable (numeric):", numeric_cols)
    factor_cols = st.multiselect("Select Factor Columns (categorical):", categorical_cols)

    # Step 3: If enough selections, build formula and run ANOVA
    if response_col and factor_cols:
        # Build ANOVA formula dynamically
        interaction_terms = ' * '.join([f'C({col})' for col in factor_cols])
        formula = f"{response_col} ~ {interaction_terms}"

        st.markdown(f"📘 **ANOVA Formula:** `{formula}`")

        try:
            model = ols(formula, data=df).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            st.success("✅ ANOVA Results:")
            st.dataframe(anova_table)
        except Exception as e:
            st.error(f"❌ Error running ANOVA: {e}")

        try:
            # Perform ANOVA with pingouin
            anova_table = pg.anova(
                dv=response_col,
                between=factor_cols if len(factor_cols) > 1 else factor_cols[0],
                data=df,
                detailed=True
            )
            st.success("✅ ANOVA Results (Pingouin):")


            

            st.dataframe(anova_table, hide_index=True)

        except Exception as e:
            st.error(f"❌ Error running ANOVA: {e}")

else:
    st.info("No CSV uploaded. Please upload a CSV to proceed. Format: one column per factor, no response column.")

