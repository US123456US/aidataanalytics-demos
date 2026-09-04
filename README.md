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


Deploying to Streamlit Community Cloud — step-by-step (one-click)

Follow these steps to deploy the Streamlit demo online using Streamlit Community Cloud (share.streamlit.io):

1. Open the Streamlit badge in this README or go to:
   https://share.streamlit.io/US123456US/aidataanalytics-demos/main/streamlit_app.py

2. If you are not signed in to Streamlit, click Sign in and choose "Sign in with GitHub". Allow Streamlit the requested GitHub permissions to read your repositories (this is required so Streamlit can fetch and build the app from this repo).

3. After logging in, you will see a Streamlit deploy page. Click "Deploy an app" or "New app":
   - Repository: select `US123456US/aidataanalytics-demos`
   - Branch: `main`
   - File path: `/streamlit_app.py`
   - Requirements file: `requirements.txt` (Streamlit will automatically install dependencies listed here)

4. Click Deploy. Streamlit will build the app by creating an environment and installing packages from requirements.txt. The build logs will be shown on the page.

5. When the build completes you will see the live app URL. Click it to open the app in your browser. The app will stay running on Streamlit Community Cloud until you stop it or the free quota is reached.

Checking build logs and troubleshooting

- Where to find logs: On the Streamlit app page click "Logs" or "View logs" to inspect the build and runtime logs.
- Common issue: Installation of `prophet` fails during build.
  - Cause: prophet (and its dependency pystan) may require a C++ build toolchain and specific binary wheels. On some systems (or on Streamlit's builder) pip will try to compile from source and fail.

Fixes and alternatives:

A. (Quick) Re-run the build: sometimes transient network or pip cache issues cause failures — click "Rebuild".

B. (Reliable) Use an alternative time-series library that doesn't require heavy compilation. I can update the Streamlit app to use `statsmodels` or `sktime` for forecasting. This usually resolves build issues because those packages have lighter or already-available wheels.

C. (Portable) Use a prebuilt Docker image and deploy to a container-friendly host (Render / Fly / Railway). I can add a Dockerfile and GitHub Actions workflow that builds the container and pushes it to GitHub Container Registry — then you can deploy the container directly (very reliable). This avoids Streamlit Cloud build problems.

D. (Advanced/local LLM) If you want full local LLM inference or heavy compiled libraries, run locally in a machine you control (or a VM) where you can install build tools (gcc, g++, python-dev). Steps for local setup are below.

Local setup (if you prefer to run locally)

1. Clone the repo:
   git clone https://github.com/US123456US/aidataanalytics-demos
   cd aidataanalytics-demos

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate

3. Install requirements:
   pip install -r requirements.txt

   If `prophet` fails to install on your platform, try one of:
   - Install build tools first (Ubuntu/Debian): sudo apt-get update && sudo apt-get install -y build-essential python3-dev libatlas-base-dev
   - Or replace prophet in requirements and the app with statsmodels and I can update code for you.

4. Run the app:
   streamlit run streamlit_app.py

What I already did for you

- Added the Streamlit badge that points to the app on share.streamlit.io
- Uploaded streamlit_app.py and requirements.txt and small example data files
- Wrote this deployment and troubleshooting guide into README

What I can do next (say which you want me to do)

1) Update the Streamlit app to use `statsmodels` (or other lightweight forecasting) so build on Streamlit Cloud is more reliable — I will update code and requirements and push a new commit. Reply: "Use statsmodels" or "Use sktime" to choose.

2) Add a Dockerfile + GitHub Actions workflow to build and publish a container image to GitHub Container Registry (ghcr.io) and include deploy instructions for Render/Fly. Reply: "Add Docker" to proceed.

3) I can also integrate PandasAI or an on-device open-source LLM (llama-cpp-python) into the Streamlit UI to enable natural-language queries of data; note local LLMs require model files and enough CPU/GPU. Reply: "Add PandasAI" if you'd like that.

4) If you'd rather I deploy the Streamlit app for you to my own Streamlit account for testing, I can deploy a public demo and share the URL (only for testing). Reply: "Deploy test demo".

---

Files in this repo:
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
