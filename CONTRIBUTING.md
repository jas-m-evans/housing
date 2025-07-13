# Contributing to DwellWell

- Use **Python 3.11**.
- Follow **PEP 8** style guidelines. Run `ruff --fix .` before committing.
- Run the test suite with `pytest -q`.
- Never commit secrets or credentials. Use environment variables or `.env` files excluded via `.gitignore`.
- Monetary values should be handled in **CAD cents** to avoid floating point issues.
