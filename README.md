# Dwelly

[![CI](https://github.com/jas-m-evans/housing/actions/workflows/ci.yml/badge.svg)](https://github.com/jas-m-evans/housing/actions/workflows/ci.yml)

Dwelly is a Streamlit app for evaluating the purchase of a two-bedroom, two-bathroom condo in downtown Vancouver. It calculates key financial metrics using user inputs and includes Monte Carlo simulations to explore different market scenarios.

Listings live in the UI.

All PRs are auto-linted & tested via GitHub Actions.

## Running the app

1. Install dependencies with `pip install -r requirements.txt`.
2. Execute `streamlit run app.py`.
3. Run `ruff --fix .` and `pytest -q` before committing changes.

## Usage
- Adjust the sidebar parameters or pick a listing, then click **Run Simulation** to generate
  projected cash flow and equity charts.
