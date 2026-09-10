# ContentPulse AI — Website Content Analyzer & Refresh Recommendation

ContentPulse AI helps content teams identify pages that need attention, prioritize refresh opportunities, and turn performance data into practical recommendations.

## Highlights

- Review page performance and refresh priority at a glance
- Filter pages by high, medium, and low priority
- Inspect content age, traffic, CTR, engagement, and quality signals
- Generate refresh-score predictions through the FastAPI service
- Explore recommended pages in the Streamlit dashboard

## Run locally

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the Streamlit dashboard:

```powershell
streamlit run app.py
```

The dashboard loads the trained model locally, so it does not require a separate API process.

The optional FastAPI service can be started separately for API clients:

```powershell
uvicorn api:app --reload
```

Then open the local Streamlit URL shown in the terminal.
