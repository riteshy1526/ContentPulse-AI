import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="ContentPulse AI — Website Content Analyzer & Refresh Recommendation",
    page_icon="📊",
    layout="wide"
)

st.title("ContentPulse AI — Website Content Analyzer & Refresh Recommendation")
st.subheader("AI-Powered Content Performance & Refresh Recommendation")


@st.cache_resource
def load_model():
    return joblib.load("models/content_priority_model.pkl")


model = load_model()

# Load dataset
df = pd.read_csv("data/content_data.csv")

# Dataset Overview
st.write("### Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Pages", len(df))

with col2:
    st.metric(
        "High Priority",
        int((df["priority"] == "High").sum())
    )

with col3:
    st.metric(
        "Medium Priority",
        int((df["priority"] == "Medium").sum())
    )


# Priority Filter
st.write("### Filter Pages by Priority")

priority_filter = st.selectbox(
    "Select Priority",
    ["All", "High", "Medium", "Low"]
)

if priority_filter == "All":
    filtered_df = df
else:
    filtered_df = df[df["priority"] == priority_filter]

st.dataframe(filtered_df)


# Recommended Pages
st.write("### Pages Recommended for Refresh")

high_priority = df[
    df["priority"] == "High"
].sort_values(
    by="refresh_score",
    ascending=False
)

st.dataframe(
    high_priority[
        [
            "page_id",
            "refresh_score",
            "content_age_days",
            "days_since_update",
            "monthly_traffic",
            "ctr",
            "engagement_rate",
            "content_quality",
            "priority"
        ]
    ].head(20)
)


# Chart
st.write("### Refresh Score Distribution")

st.bar_chart(
    df["refresh_score"].value_counts(bins=10).sort_index()
)


# Analyze a Page
st.write("### 🔎 Analyze a Page")

selected_page = st.selectbox(
    "Select a Page",
    df["page_id"].tolist()
)

selected_data = df[
    df["page_id"] == selected_page
].iloc[0]


# Page Details
st.write("#### Page Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Refresh Score",
        round(selected_data["refresh_score"], 2)
    )

with col2:
    st.metric(
        "Priority",
        selected_data["priority"]
    )

with col3:
    st.metric(
        "Monthly Traffic",
        int(selected_data["monthly_traffic"])
    )


# Local ML Prediction
st.write("### 🧠 ML Model Prediction")

model_input = pd.DataFrame([{
    "word_count": int(selected_data["word_count"]),
    "content_age_days": int(selected_data["content_age_days"]),
    "days_since_update": int(selected_data["days_since_update"]),
    "monthly_traffic": int(selected_data["monthly_traffic"]),
    "search_volume": int(selected_data["search_volume"]),
    "avg_position": float(selected_data["avg_position"]),
    "ctr": float(selected_data["ctr"]),
    "engagement_rate": float(selected_data["engagement_rate"]),
    "bounce_rate": float(selected_data["bounce_rate"]),
    "backlinks": int(selected_data["backlinks"]),
    "content_quality": float(selected_data["content_quality"])
}])

prediction = model.predict(model_input)[0]
refresh_score = (
    (selected_data["content_age_days"] / 1500) * 0.20
    + (selected_data["days_since_update"] / 900) * 0.20
    + (1 - selected_data["engagement_rate"]) * 0.15
    + selected_data["bounce_rate"] * 0.15
    + (1 - selected_data["content_quality"]) * 0.15
    + (1 - selected_data["ctr"] / 0.25) * 0.15
)
refresh_score = max(0, min(1, refresh_score))

st.info(f"Model Prediction: **{prediction}**")
st.write(f"ML Refresh Score: **{round(refresh_score, 2)}**")


# AI Recommendation
st.write("### 🤖 AI Recommendation")

if selected_data["refresh_score"] >= 0.65:

    st.error(
        "🔴 High Priority: This page should be refreshed soon."
    )

elif selected_data["refresh_score"] >= 0.35:

    st.warning(
        "🟡 Medium Priority: This page may need improvement."
    )

else:

    st.success(
        "🟢 Low Priority: This page is performing well."
    )
