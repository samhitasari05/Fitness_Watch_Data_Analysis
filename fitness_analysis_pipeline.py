##Fitness Insights and Activity Segmentation Using Wearable Data

##Step 1: Load the Data and install required libraries

!pip install plotly
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "/home/ssariko/Market_Basket_Analysis/Apple-Fitness-Data.csv"  # Replace with your file path
fitness_data = pd.read_csv(file_path)

# Display basic information about the dataset
print("Dataset Overview:")
print(fitness_data.info())
print("\nFirst Few Rows:")
print(fitness_data.head())

##Step 2: Data Cleaning

# Convert Date to datetime format
fitness_data['Date'] = pd.to_datetime(fitness_data['Date'])

# Remove trailing spaces in the Time column
fitness_data['Time'] = fitness_data['Time'].str.strip()

# Convert Time to datetime.time format
fitness_data['Time'] = pd.to_datetime(fitness_data['Time'], format='%H:%M:%S').dt.time

# Combine Date and Time into a single Datetime column
fitness_data['Datetime'] = pd.to_datetime(fitness_data['Date'].astype(str) + ' ' + fitness_data['Time'].astype(str))

# Drop unnecessary columns if needed
# fitness_data = fitness_data.drop(columns=['Date', 'Time'])  # Uncomment if Date and Time columns are no longer needed it's of user's choice

# Verify the changes
print("\nCleaned Data Overview:")
print(fitness_data.head())

##Step 3: Exploratory Data Analysis (EDA)

#Correlation Heatmap

# Plot correlation heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = fitness_data.drop(columns=['Date', 'Time', 'Datetime']).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

#Time Series Analysis

# Plot Step Count and Energy Burned over time
plt.figure(figsize=(12, 6))
plt.plot(fitness_data['Datetime'], fitness_data['Step Count'], label='Step Count', alpha=0.7)
plt.plot(fitness_data['Datetime'], fitness_data['Energy Burned'], label='Energy Burned', alpha=0.7)
plt.xlabel("Datetime")
plt.ylabel("Values")
plt.title("Time-Series Analysis of Step Count and Energy Burned")
plt.legend()
plt.show()

##Step 4: Feature ENgineering and Modeling

# Create a new column for Energy Burned per Step
fitness_data['Energy per Step'] = fitness_data['Energy Burned'] / fitness_data['Step Count']
fitness_data['Energy per Step'].fillna(0, inplace=True)  
print("\nNew Feature Added: Energy Burned per Step")
print(fitness_data.head())

import plotly.express as px

# Interactive scatter plot for Step Count vs Energy Burned
fig = px.scatter(
    fitness_data,
    x='Step Count',
    y='Energy Burned',
    color='Walking Speed',
    size='Distance',
    hover_data=['Datetime'],
    title="Interactive Scatter Plot: Step Count vs Energy Burned"
)
fig.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Select features for clustering
features = fitness_data[['Step Count', 'Distance', 'Energy per Step']]

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
fitness_data['Fitness Level'] = kmeans.fit_predict(scaled_features)

# Cluster Summary
print("Cluster Distribution:")
print(fitness_data['Fitness Level'].value_counts())

# Visualize Clusters: Energy per Step vs Step Count
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=fitness_data['Step Count'],
    y=fitness_data['Energy per Step'],
    hue=fitness_data['Fitness Level'],
    palette='viridis'
)
plt.title("Clustering Results: Step Count vs Energy per Step")
plt.xlabel("Step Count")
plt.ylabel("Energy per Step")
plt.legend(title="Fitness Level")
plt.show()

# Analyze clusters by summarizing key statistics
cluster_summary = fitness_data.groupby('Fitness Level').agg({
    'Step Count': ['mean', 'std'],
    'Energy per Step': ['mean', 'std'],
    'Distance': ['mean', 'std']
}).reset_index()

print("Cluster Summary:")
print(cluster_summary)

recommendations = {
    0: "Low activity users: Increase daily steps to improve fitness levels.",
    1: "Moderate activity users: Maintain consistency, focus on improving energy efficiency.",
    2: "High energy users: Monitor for potential overexertion or unusual activity patterns."
}

for cluster, advice in recommendations.items():
    print(f"Cluster {cluster}: {advice}")

