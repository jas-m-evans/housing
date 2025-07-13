import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="DwellWell", layout="wide")

st.sidebar.header("Input Parameters")

purchase_price = st.sidebar.number_input(
    "Purchase Price (CAD)", min_value=0, step=1_000
)
down_payment_pct = st.sidebar.number_input(
    "Down Payment (%)", min_value=0.0, max_value=100.0, value=20.0
)
interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, value=5.0)
strata_fee = st.sidebar.number_input("Monthly Strata Fee (CAD)", min_value=0, step=10)
property_tax = st.sidebar.number_input(
    "Annual Property Tax (CAD)", min_value=0, step=100
)
expected_rent = st.sidebar.number_input(
    "Expected Monthly Rent (CAD)", min_value=0, step=10
)
vacancy_pct = st.sidebar.number_input(
    "Vacancy Rate (%)", min_value=0.0, max_value=100.0, value=2.0
)
scenario = st.sidebar.selectbox("Scenario", ["Live-in", "Rent-out"])

st.title("DwellWell")

st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Mortgage", "0")
col2.metric("Net Cash Flow", "0")
col3.metric("ROI", "0")

# TODO: Plug in Monte Carlo simulation results here

st.header("Projections")
empty_df = pd.DataFrame({"x": [], "y": []})
line_chart = alt.Chart(empty_df).mark_line().encode(x="x", y="y")
bar_chart = alt.Chart(empty_df).mark_bar().encode(x="x", y="y")

st.altair_chart(line_chart, use_container_width=True)
st.altair_chart(bar_chart, use_container_width=True)
