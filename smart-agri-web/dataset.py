"""
dataset.py
-----------
Loads and processes the Smart Agriculture dataset.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "cropdata_updated.csv")


def load_dataset():
    """Load the dataset."""
    return pd.read_csv(DATASET_PATH)


def get_crop_list(df):
    """Return the sorted list of unique crops available in the dataset."""
    return sorted(df["crop ID"].dropna().unique().tolist())


def get_soil_list(df):
    """Return the sorted list of unique soil types available in the dataset."""
    return sorted(df["soil_type"].dropna().unique().tolist())


def get_crop_data(df, crop_name):
    """Return all records for the selected crop."""

    crop = df[df["crop ID"].str.lower() == crop_name.lower()]

    if crop.empty:
        return None

    return crop


def get_average_conditions(df, crop_name):
    """Return average values for a crop."""

    crop = get_crop_data(df, crop_name)

    if crop is None:
        return None

    return {
        "Temperature": round(crop["temp"].mean(), 2),
        "Humidity": round(crop["humidity"].mean(), 2),
        "Moisture Index": round(crop["MOI"].mean(), 2),
        "Soil Type": crop["soil_type"].mode()[0],
        "Seedling Stage": crop["Seedling Stage"].mode()[0],
        "Irrigation": "Yes" if crop["result"].mode()[0] == 1 else "No"
    }
