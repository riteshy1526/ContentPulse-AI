import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/content_data.csv")

# Basic information
print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())

print("\nPriority Distribution:")
print(df["priority"].value_counts())

# Refresh score distribution
plt.figure(figsize=(8, 5))
plt.hist(df["refresh_score"], bins=30)
plt.xlabel("Refresh Score")
plt.ylabel("Number of Pages")
plt.title("Content Refresh Score Distribution")
plt.show()

# Priority distribution
df["priority"].value_counts().plot(kind="bar")
plt.xlabel("Priority")
plt.ylabel("Number of Pages")
plt.title("Content Priority Distribution")
plt.show()