# AI Data Analytics Demos

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/US123456US/aidataanalytics-demos/main/streamlit_app.py)

This repository contains three runnable, open-source demos for AI-powered data analytics (fully free/open-source components). Demos:

- Streamlit interactive demo (streamlit_app.py)
- Jupyter notebook demo (notebooks/analysis.ipynb) + Voila instructions
- TimescaleDB + Grafana demo (docker-compose.yml) with a simple Python backend that ingests synthetic time series and runs forecasts

Each demo includes a small example dataset and quick start instructions below.

Quick start (recommended order)

1) Streamlit demo (interactive)
   - Click the badge above to open the app on Streamlit Community Cloud (you may need to log into Streamlit). Or run locally:
     - Install: python -m pip install -r requirements.txt
     - Run: streamlit run streamlit_app.py

2) Jupyter demo
   - Install: python -m pip install -r requirements-notebook.txt
   - Run: jupyter notebook notebooks/analysis.ipynb  (or use Binder/Voila if configured)

3) TimescaleDB + Grafana demo (Docker Compose)
   - Requires Docker & Docker Compose
   - Run: docker-compose up --build
   - The backend will ingest sample data into TimescaleDB and write forecast results. Grafana will be available on port 3000. Default Grafana login: admin/admin (you will be asked to change it on first login)

Notes on "AI" features
- The demos include time-series forecasting using the open-source Prophet library (Facebook/Meta Prophet). It provides automatic trend and seasonality modeling.
- For natural-language DataFrame querying we provide optional hooks for PandasAI or other LLMs; if you want fully local LLM-based reasoning I can add instructions for using llama-cpp-python or a local model image.

If you want, I can also enable GitHub Actions to build and publish a demo container or connect a Streamlit Cloud launch button.

---

Files in this commit:
- streamlit_app.py
- requirements.txt
- requirements-notebook.txt
- notebooks/analysis.ipynb
- docker-compose.yml
- timeseries_ingest_and_analyze.py
- grafana_dashboard.json
- data/stock_aapl_sample.csv
- data/iot_sensor_sample.csv
- README.md (this file)
