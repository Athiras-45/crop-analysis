"""
soil.py
--------
Compares the farm's actual soil type against
the crop's ideal soil type (from the dataset).
"""


def compare_soil(farm_soil_type, ideal_soil_type):
    """Return whether farm soil matches the crop's ideal soil type."""

    if not farm_soil_type or not ideal_soil_type:
        return "Unknown"

    farm_soil_type = farm_soil_type.strip().lower()
    ideal_soil_type = ideal_soil_type.strip().lower()

    if farm_soil_type == ideal_soil_type:
        return "Match"

    return "Mismatch"
