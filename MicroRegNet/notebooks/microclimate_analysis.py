"""
Microclimate & Weather Combined Analysis
Run this from the project root:  python notebooks/microclimate_analysis.py
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from preprocess import load_and_merge_all
from model import run_clustering

# =========================
# 1. Load Data
# =========================
df = load_and_merge_all()
print("Merged dataset shape:", df.shape)

# =========================
# 2. Clustering
# =========================
clustered_df, model, used_features = run_clustering(df, n_clusters=5)
print(f"\nClustering complete using {len(used_features)} features:")
print(used_features)
print("\nCluster counts:")
print(clustered_df['cluster'].value_counts())

# =========================
# 3. Visualization
# =========================
os.makedirs("outputs", exist_ok=True)

# Static plot (first 2 features)
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=clustered_df[used_features[0]],
    y=clustered_df[used_features[1]],
    hue=clustered_df['cluster'],
    palette='Set2'
)
plt.title("Environmental Clustering Results")
plt.xlabel(used_features[0])
plt.ylabel(used_features[1])
plt.tight_layout()
plt.savefig("outputs/combined_clustering_results.png")
plt.close()

# Interactive plot
fig = px.scatter(
    clustered_df,
    x=used_features[0],
    y=used_features[1],
    color='cluster',
    title="Interactive Combined Cluster Plot",
    hover_data=['datetime', 'lulc_type'] if 'lulc_type' in clustered_df.columns else ['datetime']
)
fig.write_html("outputs/combined_cluster_plot.html")

print("\nAnalysis complete. Outputs saved in 'outputs/' folder.")