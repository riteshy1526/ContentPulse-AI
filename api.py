from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="ContentPulse AI — Website Content Analyzer & Refresh Recommendation")

# Load trained ML model
model = joblib.load("models/content_priority_model.pkl")


class PageData(BaseModel):
    word_count: int
    content_age_days: int
    days_since_update: int
    monthly_traffic: int
    search_volume: int
    avg_position: float
    ctr: float
    engagement_rate: float
    bounce_rate: float
    backlinks: int
    content_quality: float


@app.get("/")
def root():
    return {
        "message": "ContentPulse AI is running"
    }


@app.post("/predict")
def predict(data: PageData):

    input_df = pd.DataFrame([data.model_dump()])

    # ML prediction
    prediction = model.predict(input_df)[0]

    # Calculate refresh score
    refresh_score = (
        (data.content_age_days / 1500) * 0.20
        + (data.days_since_update / 900) * 0.20
        + (1 - data.engagement_rate) * 0.15
        + data.bounce_rate * 0.15
        + (1 - data.content_quality) * 0.15
        + (1 - data.ctr / 0.25) * 0.15
    )

    refresh_score = max(0, min(1, refresh_score))

    return {
        "prediction": prediction,
        "refresh_score": round(refresh_score, 2)
    }