"""
Preprocessing logic for multi-source environmental datasets.
"""

import pandas as pd

def load_and_clean_microclimate(filepaths):
    """Load and combine multiple microclimate datasets."""
    dfs = []
    for path in filepaths:
        df = pd.read_csv(path)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # Ensure timestamp is datetime
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        dfs.append(df)
    
    # Combine all microclimate datasets
    micro_df = pd.concat(dfs, ignore_index=True)
    micro_df.drop_duplicates(inplace=True)
    return micro_df


def load_and_clean_weather(filepath):
    """Load and clean the weather dataset."""
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Ensure date is datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


def merge_datasets(micro_df, weather_df):
    """
    Merge microclimate and weather datasets on timestamp.
    Handles different column names for time.
    """
    # Rename for join
    micro_df = micro_df.rename(columns={"timestamp": "datetime"})
    weather_df = weather_df.rename(columns={"date": "datetime"})
    
    merged = pd.merge(
        micro_df, weather_df,
        on="datetime",
        how="outer",  # Keep all records
        suffixes=("_micro", "_weather")
    )
    return merged


def load_and_merge_all():
    """Main function to load, clean, and merge all datasets."""
    # File paths
    micro_paths = [
        "data/Microclimate_dataset.csv",
        "data/simulated_microclimate_dataset.csv"
    ]
    weather_path = "data/cleaned_weather.csv"
    
    # Load datasets
    micro_df = load_and_clean_microclimate(micro_paths)
    weather_df = load_and_clean_weather(weather_path)
    
    # Merge
    merged_df = merge_datasets(micro_df, weather_df)
    
    # Drop rows without any meaningful data
    merged_df.dropna(how="all", inplace=True)
    
    return merged_df