"""
analysis.py
------------
Compares live farm/weather conditions against ideal
crop conditions and produces an analysis summary.
"""

from soil import compare_soil


def analyze_farm(farm_data, weather_data, dataset_data, satellite_data=None):

    analysis = {}

    # Compare Temperature
    if weather_data["Temperature"] > dataset_data["Temperature"]:
        analysis["Temperature"] = "Higher than ideal"

    elif weather_data["Temperature"] < dataset_data["Temperature"]:
        analysis["Temperature"] = "Lower than ideal"

    else:
        analysis["Temperature"] = "Ideal"

    # Compare Humidity
    if weather_data["Humidity"] > dataset_data["Humidity"]:
        analysis["Humidity"] = "Higher than ideal"

    elif weather_data["Humidity"] < dataset_data["Humidity"]:
        analysis["Humidity"] = "Lower than ideal"

    else:
        analysis["Humidity"] = "Ideal"

    analysis["Soil Type (Ideal)"] = dataset_data["Soil Type"]
    analysis["Soil Type (Farm)"] = farm_data["Soil Type"]
    analysis["Soil Match"] = compare_soil(
        farm_data["Soil Type"],
        dataset_data["Soil Type"]
    )

    analysis["Moisture Index"] = dataset_data["Moisture Index"]
    analysis["Irrigation"] = dataset_data["Irrigation"]

    # Satellite-derived fields (may be None if the API call failed)
    if satellite_data:
        analysis["NDVI"] = satellite_data["NDVI"]
        analysis["Vegetation Health"] = satellite_data["Vegetation Health"]
        analysis["Surface Temperature (Satellite)"] = satellite_data["Surface Temperature"]
    else:
        analysis["NDVI"] = "Unavailable"
        analysis["Vegetation Health"] = "Unavailable"
        analysis["Surface Temperature (Satellite)"] = "Unavailable"

    return analysis
