# ContentPulse AI

ContentPulse AI is a website content intelligence platform for finding pages that need attention, measuring public content quality, and prioritizing refresh opportunities.

It combines a Streamlit dashboard, a FastAPI service, HTML analysis, a local machine-learning model, and a dataset exploration workflow in one practical developer project.

## What It Does

- Analyze a single public webpage.
- Crawl multiple pages from the same website.
- Extract public content and SEO signals from HTML.
- Calculate content quality and refresh opportunity scores.
- Classify pages as High, Medium, or Low priority.
- Explore the local content dataset with filters and charts.
- Run ML-assisted priority predictions for selected dataset pages.
- Display prediction confidence when the model supports probabilities.
- Download filtered dashboard results as CSV.
- Start the FastAPI backend automatically from the Streamlit app when it is unavailable.

## Product Workflow

1. Enter a public page or website URL.
2. ContentPulse AI fetches the HTML with a descriptive user agent.
3. The analyzer extracts titles, meta descriptions, text, headings, links, images, and missing image alt text.
4. Public content signals are converted into quality and refresh scores.
5. Pages are assigned a refresh priority.
6. The dashboard presents the findings as metrics, tables, charts, recommendations, and downloadable data.

## Architecture

```text
Streamlit dashboard (app.py)
				|
				| HTTP requests
				v
FastAPI service (api.py)
				|
				+-- Single-page HTML analyzer
				+-- Same-domain website crawler
				+-- ML priority prediction endpoint
				|
				+-- Local Random Forest model
				+-- Local CSV dataset
```

### Main components

- `app.py`: Streamlit user interface, dataset dashboard, API integration, model prediction, CSV export, and automatic API startup.
- `api.py`: FastAPI endpoints for ML prediction, single-page analysis, and multi-page crawling.
- `models/content_priority_model.pkl`: Trained Random Forest classifier.
- `data/content_data.csv`: Local content-performance dataset used by the dashboard and model training.
- `src/train_model.py`: Rebuilds the model from the current dataset.
- `tests/`: Project test location.

## Requirements

- Python 3.10 or newer
- Internet access for analyzing public URLs
- A public webpage must allow the request to complete successfully

Install the dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

## Run the Dashboard

Start the Streamlit app:

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

The app checks port `8000` automatically and starts the FastAPI service in the background when needed. You normally do not need to open a second terminal for Uvicorn.

## Run the API Separately

Run the API manually when developing or testing API clients:

```powershell
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

The API root should return:

```json
{
	"message": "ContentPulse AI API is running",
	"version": "2.0"
}
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `GET /`

Returns the API health response.

### `POST /predict`

Predicts page priority from content and performance features.

Example request:

```json
{
	"word_count": 1800,
	"content_age_days": 420,
	"days_since_update": 180,
	"monthly_traffic": 12500,
	"search_volume": 5400,
	"avg_position": 18.4,
	"ctr": 0.042,
	"engagement_rate": 0.31,
	"bounce_rate": 0.58,
	"backlinks": 120,
	"content_quality": 0.72
}
```

### `POST /analyze-url`

Analyzes one public webpage.

```json
{
	"url": "https://example.com/article"
}
```

The response includes the page title, meta description, word count, heading count, internal and external links, image counts, quality score, refresh score, and priority.

### `POST /analyze-website`

Crawls pages on the same domain.

```json
{
	"url": "https://example.com",
	"max_pages": 10
}
```

The crawler is limited to 25 pages per request and returns analyzed pages, priority totals, and the pages with the highest refresh opportunity.

## Rebuild the ML Model

The model is trained from `data/content_data.csv` using the feature columns defined in `src/train_model.py`.

```powershell
python src/train_model.py
```

The command saves the model to:

```text
models/content_priority_model.pkl
```

After rebuilding the model, restart Streamlit so the new artifact is loaded.

## Model Features

The classifier uses:

- `word_count`
- `content_age_days`
- `days_since_update`
- `monthly_traffic`
- `search_volume`
- `avg_position`
- `ctr`
- `engagement_rate`
- `bounce_rate`
- `backlinks`
- `content_quality`

The model supports prioritization decisions; it is not a replacement for editorial review, analytics attribution, or search-engine data.

## Data and Privacy

ContentPulse AI analyzes publicly accessible HTML. It does not automatically access private Google Analytics, Google Search Console, backlink platforms, conversion data, authenticated pages, or private company systems.

Only submit URLs that you are authorized to analyze. Respect the target website's terms, rate limits, and access policies.

## Troubleshooting

### Streamlit shows a connection error

Use the active Streamlit URL from the terminal, normally `http://localhost:8501`. Temporary test ports such as `8502` or `8503` may be closed after verification.

### The API status shows offline

Refresh the page once. The dashboard automatically attempts to start Uvicorn on port `8000`. You can also verify the service directly:

```powershell
Invoke-WebRequest http://127.0.0.1:8000
```

### The model is missing or cannot be loaded

Rebuild it with the current environment:

```powershell
python src/train_model.py
```

Then restart Streamlit.

### A URL analysis fails

Check that the URL is public, uses a valid domain, responds within the request timeout, and is not blocking automated requests.

## Development Checks

Run the Python syntax check before committing changes:

```powershell
python -m py_compile app.py api.py src/train_model.py
```

## Project Status

ContentPulse AI is a local development and demonstration platform. It is suitable for prototyping content audits, refresh prioritization workflows, and public-page analysis. Production deployment should add authentication, request rate limiting, structured logging, stronger URL validation, background jobs for long crawls, and persistent storage for analysis history.
