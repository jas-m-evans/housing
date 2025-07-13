# DwellWell

DwellWell is a Streamlit app for evaluating the purchase of a two-bedroom, two-bathroom condo in downtown Vancouver. It calculates key financial metrics using user inputs and will eventually include Monte Carlo simulations to explore different market scenarios.

## Running the app

1. Install dependencies with `pip install -r requirements.txt`.
2. Execute `streamlit run app.py`.
3. Run `ruff --fix .` and `pytest -q` before committing changes.

## Usage
- You can upload a CSV of listings to pre-fill deal variables.
- Adjust the sidebar parameters then click **Run Simulation** to generate
  projected cash flow and equity charts.
