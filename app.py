import altair as alt
import streamlit as st

from models import key_metrics, mortgage_payment, simulate_property
from utils import coerce_numeric_fields

DEFAULTS = dict(
    purchase_price=750000,
    down_payment_pct=20.0,
    interest_rate=5.0,
    strata_fee=450,
    property_tax=2201,
    expected_rent=3270,
    vacancy_pct=2.0,
    scenario="Live-in",
    selected_listing=None,
)


def fmt_money(x: float | int, cents: bool = False) -> str:
    v = (x / 100.0) if cents else float(x)
    return f"${v:,.0f}"


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

for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

st.title("Dwelly")

with st.expander("Manage Listings"):
    listings = st.session_state["listings"]
    labels = [f"{lst['address']} – ${lst['list_price']}" for lst in listings]
    options = [None] + list(range(len(listings)))

    def format_option(i: int | None) -> str:
        return "Custom inputs (no listing)" if i is None else labels[i]

    selected_index = st.selectbox(
        "Selected listing", options, key="selected_listing", format_func=format_option
    )

    if selected_index is not None:
        listing = listings[selected_index]
        fields = {
            "purchase_price": listing["list_price"],
            "strata_fee": listing["strata_fee"],
            "property_tax": listing["property_tax"],
            "expected_rent": listing["expected_rent"],
        }
        if any(st.session_state[k] != v for k, v in fields.items()):
            st.session_state.update(fields)
            st.rerun()
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
        st.session_state.update(
            {
                "selected_listing": len(st.session_state["listings"]) - 1,
                "purchase_price": new_listing["list_price"],
                "strata_fee": new_listing["strata_fee"],
                "property_tax": new_listing["property_tax"],
                "expected_rent": new_listing["expected_rent"],
            }
        )
        st.toast("Listing added")
        st.rerun()
    elif update and selected_index is not None:
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
        st.session_state.update(
            {
                "purchase_price": updated_listing["list_price"],
                "strata_fee": updated_listing["strata_fee"],
                "property_tax": updated_listing["property_tax"],
                "expected_rent": updated_listing["expected_rent"],
            }
        )
        st.toast("Listing updated")
        st.rerun()
    elif delete and selected_index is not None:
        st.session_state["listings"].pop(selected_index)
        for key in ["purchase_price", "strata_fee", "property_tax", "expected_rent"]:
            st.session_state[key] = DEFAULTS[key]
        st.session_state["selected_listing"] = None
        st.toast("Listing deleted")
        st.rerun()

st.sidebar.header("Input Parameters")

st.sidebar.number_input(
    "Purchase Price (CAD)", min_value=0, step=1000, key="purchase_price"
)
st.sidebar.number_input(
    "Down Payment (%)", min_value=0.0, max_value=100.0, key="down_payment_pct"
)
st.sidebar.number_input(
    "Interest Rate (%)", min_value=0.0, key="interest_rate"
)
st.sidebar.number_input(
    "Monthly Strata Fee (CAD)", min_value=0, step=10, key="strata_fee"
)
st.sidebar.number_input(
    "Annual Property Tax (CAD)", min_value=0, step=100, key="property_tax"
)
st.sidebar.number_input(
    "Expected Monthly Rent (CAD)", min_value=0, step=10, key="expected_rent"
)
st.sidebar.number_input(
    "Vacancy Rate (%)", min_value=0.0, max_value=100.0, key="vacancy_pct"
)
st.sidebar.selectbox(
    "Scenario", options=["Live-in", "Rent-out"], key="scenario"
)

st.header("Key Metrics")
run_col, reset_col = st.columns(2)
run_clicked = run_col.button("Run Simulation")
if reset_col.button("Reset inputs"):
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.rerun()
st.caption("Pick a listing or use custom inputs.")
col1, col2, col3 = st.columns(3)

if run_clicked:
    price = int(st.session_state["purchase_price"])
    rent = int(st.session_state["expected_rent"])
    if price == 0 or rent == 0:
        st.warning("Please enter values or pick a listing.")
    else:
        down = float(st.session_state["down_payment_pct"]) / 100.0
        rate = float(st.session_state["interest_rate"]) / 100.0
        strata = int(st.session_state["strata_fee"])
        tax = int(st.session_state["property_tax"])
        vac = float(st.session_state["vacancy_pct"]) / 100.0

        df = simulate_property(
            n_sim=1000,
            horizon_years=10,
            price=price,
            rent=rent,
            down_pct=down,
            annual_rate=rate,
            strata_fee=strata,
            property_tax=tax,
            vacancy_pct=vac,
        )
        metrics = key_metrics(df)

        mortgage = mortgage_payment(
            principal=price * (1 - down),
            annual_rate=rate,
            amort_years=25,
        )
        col1.metric("Monthly Mortgage", fmt_money(mortgage, cents=True))
        col2.metric("Median Year-1 Cash Flow", fmt_money(metrics["p50_cash_flow"]))
        col3.metric("Equity Year 10", fmt_money(metrics["p50_equity_year10"]))

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
