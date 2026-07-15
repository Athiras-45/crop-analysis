"""
recommendation.py
-------------------
Generates human-readable recommendations from the analysis.
"""


def generate_recommendations(analysis):

    recommendations = []

    if analysis["Temperature"] == "Higher than ideal":
        recommendations.append("Increase irrigation to reduce heat stress.")

    if analysis["Temperature"] == "Lower than ideal":
        recommendations.append("Monitor crops for cold stress.")

    if analysis["Humidity"] == "Lower than ideal":
        recommendations.append("Increase watering frequency.")

    if analysis["Irrigation"] == "Yes":
        recommendations.append("Dataset recommends irrigation.")

    if analysis["Soil Match"] == "Mismatch":
        recommendations.append(
            f"Soil mismatch: farm soil is '{analysis['Soil Type (Farm)']}' but "
            f"'{analysis['Soil Type (Ideal)']}' is ideal for this crop. "
            "Consider soil amendment or a more suitable crop."
        )
    elif analysis["Soil Match"] == "Unknown":
        recommendations.append("Soil type comparison unavailable — check inputs.")

    if analysis["Vegetation Health"] in ("Very Poor", "Poor"):
        recommendations.append(
            f"Satellite NDVI indicates {analysis['Vegetation Health'].lower()} "
            "vegetation health — inspect crop for stress or disease."
        )
    elif analysis["Vegetation Health"] == "Unavailable":
        recommendations.append("Satellite vegetation data unavailable for this location.")

    recommendations.append(f"Moisture Index: {analysis['Moisture Index']}")

    return recommendations
