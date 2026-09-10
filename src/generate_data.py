import pandas as pd
import numpy as np

np.random.seed(42)

n = 1500

data = {
    "page_id": [f"PAGE_{i:04d}" for i in range(1, n + 1)],
    "word_count": np.random.randint(500, 4000, n),
    "content_age_days": np.random.randint(30, 1500, n),
    "days_since_update": np.random.randint(30, 900, n),
    "monthly_traffic": np.random.randint(100, 50000, n),
    "search_volume": np.random.randint(100, 100000, n),
    "avg_position": np.round(np.random.uniform(1, 50, n), 2),
    "ctr": np.round(np.random.uniform(0.01, 0.25, n), 4),
    "engagement_rate": np.round(np.random.uniform(0.1, 0.95, n), 3),
    "bounce_rate": np.round(np.random.uniform(0.1, 0.9, n), 3),
    "backlinks": np.random.randint(0, 1000, n),
    "content_quality": np.round(np.random.uniform(0.2, 1.0, n), 3),
}

df = pd.DataFrame(data)

# Create a refresh priority score
df["refresh_score"] = (
    (df["content_age_days"] / 1500) * 0.20
    + (df["days_since_update"] / 900) * 0.20
    + (1 - df["engagement_rate"]) * 0.15
    + df["bounce_rate"] * 0.15
    + (1 - df["content_quality"]) * 0.15
    + (1 - df["ctr"] / 0.25) * 0.15
)

# Add small randomness
df["refresh_score"] += np.random.normal(0, 0.03, n)

df["refresh_score"] = df["refresh_score"].clip(0, 1)

# Priority category
df["priority"] = pd.cut(
    df["refresh_score"],
    bins=[-0.01, 0.35, 0.65, 1.0],
    labels=["Low", "Medium", "High"]
)

# Save dataset
df.to_csv("data/content_data.csv", index=False)

print("Dataset created successfully!")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())