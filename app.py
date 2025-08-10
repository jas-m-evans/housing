import altair as alt
import pandas as pd
import streamlit as st

from models import key_metrics, simulate_property
from utils import coerce_numeric_fields

st.set_page_config(page_title="Dwelly", layout="wide")

if "listings" not in st.session_state:
    st.session_state["listings"] = []

if not st.session_state["listings"]:
    st.session_state["listings"] = [
        {
            "address": "123 Granville St",
            "city": "Vancouver",
            "list_price": 750000,
            "bedrooms": 2.0,
            "bathrooms": 2.0,
            "sqft": 900,
            "strata_fee": 450,
            "property_tax": 2200,
            "expected_rent": 3200,
        },
        {
            "address": "456 Davie St",
            "city": "Vancouver",
            "list_price": 680000,
            "bedrooms": 1.0,
            "bathrooms": 1.0,
            "sqft": 650,
            "strata_fee": 380,
            "property_tax": 1800,
            "expected_rent": 2800,
        },
        {
            "address": "789 Howe St",
            "city": "Vancouver",
            "list_price": 820000,
            "bedrooms": 2.0,
            "bathrooms": 2.0,
            "sqft": 1000,
            "strata_fee": 500,
            "property_tax": 2500,
            "expected_rent": 3400,
        },
    ]

DEFAULTS = {
    "purchase_price": 0,
    "down_payment_pct": 20.0,
    "interest_rate": 5.0,
    "strata_fee": 0,
    "property_tax": 0,
    "expected_rent": 0,
    "vacancy_pct": 2.0,
    "scenario": "Live-in",
}

for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

st.session_state.setdefault("selected_listing", "Custom inputs (no listing)")


def reset_inputs() -> None:
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.session_state["selected_listing"] = "Custom inputs (no listing)"


st.title("Dwelly")

with st.expander("Manage Listings"):
    labels = [f"{listing['address']} – ${listing['list_price']}" for listing in st.session_state['listings']]
    options = ["Custom inputs (no listing)"] + labels
    selected_label = st.selectbox(
        "Selected listing", options, key="selected_listing"
    )
    selected_index = options.index(selected_label) - 1

    if selected_index >= 0:
        listing = st.session_state["listings"][selected_index]
        st.session_state["purchase_price"] = listing["list_price"]
        st.session_state["strata_fee"] = listing["strata_fee"]
        st.session_state["property_tax"] = listing["property_tax"]
        st.session_state["expected_rent"] = listing["expected_rent"]
    else:
        listing = {}

    with st.form("listing_form"):
        address = st.text_input("Address", value=listing.get("address", ""))
        city = st.text_input("City", value=listing.get("city", ""))
        list_price = st.number_input(
            "List Price", min_value=0, step=1000, value=listing.get("list_price", 0)
        )
        bedrooms = st.number_input(
            "Bedrooms", min_value=0.0, step=0.5, value=listing.get("bedrooms", 0.0)
        )
        bathrooms = st.number_input(
            "Bathrooms", min_value=0.0, step=0.5, value=listing.get("bathrooms", 0.0)
        )
        sqft = st.number_input(
            "Square Feet", min_value=0, step=10, value=listing.get("sqft", 0)
        )
        strata_fee = st.number_input(
            "Monthly Strata Fee", min_value=0, step=10, value=listing.get("strata_fee", 0)
        )
        property_tax = st.number_input(
            "Annual Property Tax", min_value=0, step=100, value=listing.get("property_tax", 0)
        )
        expected_rent = st.number_input(
            "Expected Monthly Rent", min_value=0, step=10, value=listing.get("expected_rent", 0)
        )
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            add = st.form_submit_button("Add Listing")
        with col_b:
            update = st.form_submit_button("Update Selected")
        with col_c:
            delete = st.form_submit_button("Delete Selected")

    if add:
        new_listing = {
            "address": address,
            "city": city,
            "list_price": list_price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft": sqft,
            "strata_fee": strata_fee,
            "property_tax": property_tax,
            "expected_rent": expected_rent,
        }
        new_listing = coerce_numeric_fields(
            new_listing,
            ["list_price", "strata_fee", "property_tax", "expected_rent", "sqft"],
        )
        st.session_state["listings"].append(new_listing)
        st.toast("Listing added")
    elif update and selected_index >= 0:
        updated_listing = {
            "address": address,
            "city": city,
            "list_price": list_price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft": sqft,
            "strata_fee": strata_fee,
            "property_tax": property_tax,
            "expected_rent": expected_rent,
        }
        updated_listing = coerce_numeric_fields(
            updated_listing,
            ["list_price", "strata_fee", "property_tax", "expected_rent", "sqft"],
        )
        st.session_state["listings"][selected_index] = updated_listing
        st.toast("Listing updated")
    elif delete and selected_index >= 0:
        st.session_state["listings"].pop(selected_index)
        st.session_state["selected_listing"] = "Custom inputs (no listing)"
        st.toast("Listing deleted")

st.sidebar.header("Input Parameters")

purchase_price = st.sidebar.number_input(
    "Purchase Price (CAD)",
    min_value=0,
    step=1000,
    key="purchase_price",
)

down_payment_pct = st.sidebar.number_input(
    "Down Payment (%)", min_value=0.0, max_value=100.0, key="down_payment_pct"
)

interest_rate = st.sidebar.number_input(
    "Interest Rate (%)", min_value=0.0, key="interest_rate"
)

strata_fee = st.sidebar.number_input(
    "Monthly Strata Fee (CAD)", min_value=0, step=10, key="strata_fee"
)

property_tax = st.sidebar.number_input(
    "Annual Property Tax (CAD)", min_value=0, step=100, key="property_tax"
)

expected_rent = st.sidebar.number_input(
    "Expected Monthly Rent (CAD)", min_value=0, step=10, key="expected_rent"
)

vacancy_pct = st.sidebar.number_input(
    "Vacancy Rate (%)", min_value=0.0, max_value=100.0, key="vacancy_pct"
)

scenario = st.sidebar.selectbox(
    "Scenario", ["Live-in", "Rent-out"], key="scenario"
)


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

st.header("Key Metrics")
run_col, reset_col = st.columns(2)
run_clicked = run_col.button("Run Simulation")
if reset_col.button("Reset inputs"):
    reset_inputs()
st.caption("Pick a listing or use custom inputs.")
col1, col2, col3 = st.columns(3)

if run_clicked:
    df = run_simulation()
    metrics = key_metrics(df)

    col1.metric("Monthly Mortgage", f"${metrics['monthly_mortgage']:.0f}")
    col2.metric("Median Year-1 Cash Flow", f"${metrics['p50_cash_flow']:.0f}")
    col3.metric("Equity Year 10", f"${metrics['p50_equity_year10']:.0f}")

    equity_stats = (
        df.groupby("year")["equity"]
        .quantile([0.1, 0.5, 0.9])
        .unstack()
        .reset_index()
        .rename(columns={0.1: "p10", 0.5: "p50", 0.9: "p90"})
    )

    line = alt.Chart(equity_stats).mark_line().encode(x="year", y="p50")
    band = alt.Chart(equity_stats).mark_area(opacity=0.3).encode(
        x="year", y="p10", y2="p90"
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
