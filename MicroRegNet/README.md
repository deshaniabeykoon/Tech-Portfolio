# Microclimate Risk Mapping

**Goal:** Analyze microclimate and environmental data to identify potential pest risk zones via clustering and visualization.

## Data Sources
- **MicroRegNet**: High-resolution microclimate data ([Kaggle Dataset](https://www.kaggle.com/datasets/ziya07/microregnet-microclimate-dataset))
- **Weather Time Series**: Atmospheric measurements including temperature, humidity, wind, etc. ([Kaggle Dataset](https://www.kaggle.com/datasets/alistairking/weather-long-term-time-series-forecasting/data))

## Structure
- `data/`: Contains raw datasets
- `notebooks/`: Exploratory and analysis notebook
- `src/`: Scripts for cleaning and modeling
- `README.md`: Project overview and instructions

## Methods
1. Exploratory data analysis  
2. Feature engineering (aggregates + risk indicators)  
3. Clustering to identify microclimate zones  
4. Visualization of patterns and clusters  

## How to Run
- Install dependencies: `pip install -r requirements.txt`  
- Run notebook or call scripts as needed
