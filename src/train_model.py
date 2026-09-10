import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/content_data.csv")

# Features
X = df[
    [
        "word_count",
        "content_age_days",
        "days_since_update",
        "monthly_traffic",
        "search_volume",
        "avg_position",
        "ctr",
        "engagement_rate",
        "bounce_rate",
        "backlinks",
        "content_quality",
    ]
]

# Target
y = df["priority"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Training
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model trained successfully!")
print("Accuracy:", round(accuracy * 100, 2), "%")

joblib.dump(model, "models/content_priority_model.pkl")

print("Model saved successfully!")