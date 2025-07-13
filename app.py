import altair as alt
import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="DwellWell", layout="wide")

uploaded_file = st.file_uploader("Upload Listings CSV", type="csv")
listings_df = None
selected_row: dict[str, object] = {}
if uploaded_file is not None:
    listings_df = pd.read_csv(uploaded_file)
    st.dataframe(listings_df)
    option_labels = listings_df.apply(
        lambda r: f"{r.get('address', '')} – ${r.get('list_price', '')}",
        axis=1,
    ).tolist()
    chosen = st.selectbox("Choose a listing", option_labels)
    idx = option_labels.index(chosen)
    selected_row = listings_df.iloc[idx].to_dict()


def default_for(key: str, fallback: float | int) -> float | int:
    val = selected_row.get(key)
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return fallback
    return val

st.sidebar.header("Input Parameters")

purchase_price = st.sidebar.number_input(
    "Purchase Price (CAD)",
    min_value=0,
    step=1_000,
    value=int(default_for("list_price", 0)),
)
down_payment_pct = st.sidebar.number_input(
    "Down Payment (%)", min_value=0.0, max_value=100.0, value=20.0
)
interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, value=5.0)
strata_fee = st.sidebar.number_input(
    "Monthly Strata Fee (CAD)",
    min_value=0,
    step=10,
    value=int(default_for("strata_fee", 0)),
)
property_tax = st.sidebar.number_input(
    "Annual Property Tax (CAD)",
    min_value=0,
    step=100,
    value=int(default_for("property_tax", 0)),
)
expected_rent = st.sidebar.number_input(
    "Expected Monthly Rent (CAD)",
    min_value=0,
    step=10,
    value=int(default_for("expected_rent", 0)),
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
