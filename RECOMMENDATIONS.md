# Recommendations for Data Trigger Bot

## 1. Implement Real Tools in `agent.py`
The current `agent.py` implementation uses template/placeholder tools (`get_weather`, `get_current_time`). Since the bot's objective in the GitHub workflow is to "Fetch the latest anomaly data from CERN, JWST, and Vera C. Rubin", formulate a digest, and push it, you need to implement actual Python functions for these tools.

Recommended new tools:
- `fetch_cern_data(query: str) -> str`
- `fetch_jwst_data(query: str) -> str`
- `fetch_vera_rubin_data(query: str) -> str`
- `push_digest(digest: str) -> str`

## 2. Update Agent System Instructions
The agent's instruction in `agent.py` is currently a generic placeholder: *"You are a helpful AI assistant designed to provide accurate and useful information."*

This should be updated to specifically describe its role in anomaly detection and reporting, e.g.:
*"You are an autonomous data trigger bot responsible for analyzing astrophysical and particle physics anomalies. Fetch the latest data from CERN, JWST, and Vera C. Rubin, formulate a digest, and push it using the available tools."*

## 3. Update GitHub Actions Workflow for `uv`
The `.github/workflows/data_trigger.yml` file uses `uv pip install --system`. In modern `uv` workflows, it is better to manage project dependencies via `uv run` and let `uv` handle the virtual environment transparently, or install the CLI tool via `uv tool install`.

Instead of running:
```bash
uv pip install --system google-agents-cli
uv pip install --system -r pyproject.toml || uv pip install --system -e .
agents-cli run ...
```

The workflow should install dependencies within the project directory using `uv sync` and run the agent via `uv run agents-cli`:
```bash
uv sync
uv run agents-cli run "Fetch the latest anomaly data from CERN, JWST, and Vera C. Rubin. Formulate a digest and execute the push tool autonomously."
```
