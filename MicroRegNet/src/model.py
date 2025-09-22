import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load datasets
micro_df = pd.read_csv("data/Microclimate_dataset.csv")
simulated_df = pd.read_csv("data/simulated_microclimate_dataset.csv")
weather_df = pd.read_csv("data/cleaned_weather.csv")

# Combine microclimate data
micro_combined = pd.concat([micro_df, simulated_df], ignore_index=True)

# Select only numeric columns for clustering
numeric_cols = micro_combined.select_dtypes(include=['float64', 'int64']).columns
data = micro_combined[numeric_cols].dropna()

# Standardize
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# PCA for visualization (2D)
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)
pca_df = pd.DataFrame(pca_data, columns=['PC1', 'PC2'])

# ---- KMeans Clustering ----
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
pca_df['KMeans_Cluster'] = kmeans.fit_predict(scaled_data)

# ---- DBSCAN Clustering ----
dbscan = DBSCAN(eps=1.5, min_samples=50)
pca_df['DBSCAN_Cluster'] = dbscan.fit_predict(scaled_data)

# ---- Plot KMeans ----
plt.figure(figsize=(8,6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='KMeans_Cluster', palette='Set1', s=10)
plt.title('KMeans Clustering on Environmental Data (PCA Projection)')
plt.legend(title="Cluster")
plt.savefig("outputs/kmeans_clusters.png")
plt.close()

# ---- Plot DBSCAN ----
plt.figure(figsize=(8,6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='DBSCAN_Cluster', palette='Set2', s=10)
plt.title('DBSCAN Clustering on Environmental Data (PCA Projection)')
plt.legend(title="Cluster")
plt.savefig("outputs/dbscan_clusters.png")
plt.close()

# ---- Interactive KMeans Plot ----
fig = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    color="KMeans_Cluster",
    title="Interactive KMeans Clustering on Environmental Data",
    color_continuous_scale="Viridis"
)
fig.write_html("outputs/kmeans_clusters_interactive.html")

# ---- Interactive DBSCAN Plot ----
fig2 = px.scatter(
    pca_df,
    x="PC1",
    y="PC2",
    color="DBSCAN_Cluster",
    title="Interactive DBSCAN Clustering on Environmental Data",
    color_continuous_scale="Turbo"
)
fig2.write_html("outputs/dbscan_clusters_interactive.html")

print("Clustering complete. Plots saved in outputs/")