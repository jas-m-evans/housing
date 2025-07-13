import altair as alt
import math
import pandas as pd
import streamlit as st

from models import key_metrics, simulate_property

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


@st.cache_data
def run_simulation() -> pd.DataFrame:
    return simulate_property(
        price=purchase_price,
        rent=expected_rent,
        down_pct=down_payment_pct,
        annual_rate=interest_rate,
        strata_fee=strata_fee,
        property_tax=property_tax,
        vacancy_pct=vacancy_pct,
    )

st.title("DwellWell")

st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

if st.button("Run Simulation"):
    df = run_simulation()
    metrics = key_metrics(df)

    col1.metric("Monthly Mortgage", f"${metrics['monthly_mortgage']:.0f}")
    col2.metric("Median Year-1 Cash Flow", f"${metrics['p50_cash_flow']:.0f}")
    col3.metric("Equity Year 10", f"${metrics['p50_equity_year10']:.0f}")

    equity_stats = (
        df.groupby("year")
        ["equity"]
        .quantile([0.1, 0.5, 0.9])
        .unstack()
        .reset_index()
        .rename(columns={0.1: "p10", 0.5: "p50", 0.9: "p90"})
    )

    line = (
        alt.Chart(equity_stats)
        .mark_line()
        .encode(x="year", y="p50")
    )
    band = (
        alt.Chart(equity_stats)
        .mark_area(opacity=0.3)
        .encode(x="year", y="p10", y2="p90")
    )
    equity_chart = band + line

    cf_hist = (
        alt.Chart(df[df["year"] == 1])
        .mark_bar()
        .encode(x=alt.X("net_cash_flow", bin=True), y="count()")
    )

    st.header("Projections")
    st.altair_chart(equity_chart, use_container_width=True)
    st.altair_chart(cf_hist, use_container_width=True)

