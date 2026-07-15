"""
app.py
-------
Flask web front-end for the Smart Agriculture Advisory System.

Replaces the old command-line input() flow (farm.py) with a web form,
and replaces the Rich console output (utils.py) with styled HTML pages.
"""

from flask import Flask, render_template, request

from dataset import load_dataset, get_average_conditions, get_crop_list, get_soil_list
from weather import get_weather
from satellite import get_satellite_data
from analysis import analyze_farm
from recommendation import generate_recommendations

app = Flask(__name__)

# Load the dataset once at startup (it doesn't change between requests)
DATASET = load_dataset()


def validate_latitude(latitude: float) -> bool:
    return -90 <= latitude <= 90


def validate_longitude(longitude: float) -> bool:
    return -180 <= longitude <= 180


@app.route("/", methods=["GET"])
def index():
    """Show the farm details input form."""
    crops = get_crop_list(DATASET)
    soils = get_soil_list(DATASET)
    return render_template("index.html", crops=crops, soils=soils, errors=[], form_data={})


@app.route("/analyze", methods=["POST"])
def analyze():
    """Validate the form, run the full pipeline, and show the report."""

    crops = get_crop_list(DATASET)
    soils = get_soil_list(DATASET)

    form_data = {
        "farm_name": request.form.get("farm_name", "").strip(),
        "farmer_name": request.form.get("farmer_name", "").strip(),
        "crop": request.form.get("crop", "").strip(),
        "soil_type": request.form.get("soil_type", "").strip(),
        "latitude": request.form.get("latitude", "").strip(),
        "longitude": request.form.get("longitude", "").strip(),
        "area": request.form.get("area", "").strip(),
    }

    errors = []

    # ---- Validate required text fields ----
    if not form_data["farm_name"]:
        errors.append("Farm Name is required.")
    if not form_data["farmer_name"]:
        errors.append("Farmer Name is required.")
    if not form_data["crop"]:
        errors.append("Please select a Crop.")
    if not form_data["soil_type"]:
        errors.append("Please select a Soil Type.")

    # ---- Validate latitude ----
    latitude = None
    try:
        latitude = float(form_data["latitude"])
        if not validate_latitude(latitude):
            errors.append("Latitude must be between -90 and 90.")
    except ValueError:
        errors.append("Latitude must be a number.")

    # ---- Validate longitude ----
    longitude = None
    try:
        longitude = float(form_data["longitude"])
        if not validate_longitude(longitude):
            errors.append("Longitude must be between -180 and 180.")
    except ValueError:
        errors.append("Longitude must be a number.")

    # ---- Validate area ----
    area = None
    try:
        area = float(form_data["area"])
        if area <= 0:
            errors.append("Farm Area must be greater than 0.")
    except ValueError:
        errors.append("Farm Area must be a number.")

    if errors:
        return render_template(
            "index.html", crops=crops, soils=soils, errors=errors, form_data=form_data
        ), 400

    farm = {
        "Farm Name": form_data["farm_name"],
        "Farmer Name": form_data["farmer_name"],
        "Crop": form_data["crop"],
        "Soil Type": form_data["soil_type"],
        "Latitude": latitude,
        "Longitude": longitude,
        "Area": area,
    }

    # ---- Crop data from dataset ----
    crop_data = get_average_conditions(DATASET, farm["Crop"])
    if crop_data is None:
        return render_template(
            "index.html", crops=crops, soils=soils,
            errors=[f"Crop '{farm['Crop']}' not found in dataset."],
            form_data=form_data
        ), 400

    # ---- Live weather ----
    weather = get_weather(farm["Latitude"], farm["Longitude"])
    if weather is None:
        return render_template(
            "index.html", crops=crops, soils=soils,
            errors=["Unable to fetch live weather data. Please try again."],
            form_data=form_data
        ), 502

    # ---- Satellite data (optional — page still renders if this fails) ----
    satellite = get_satellite_data(farm["Latitude"], farm["Longitude"])
    satellite_available = satellite is not None

    # ---- Analysis + recommendations ----
    analysis = analyze_farm(farm, weather, crop_data, satellite)
    recommendations = generate_recommendations(analysis)

    farm_summary = {
        "Farm Name": farm["Farm Name"],
        "Farmer Name": farm["Farmer Name"],
        "Crop": farm["Crop"],
        "Area (Acres)": farm["Area"],
        "Latitude": farm["Latitude"],
        "Longitude": farm["Longitude"],
    }

    return render_template(
        "results.html",
        farm_summary=farm_summary,
        crop_data=crop_data,
        weather=weather,
        satellite=satellite,
        satellite_available=satellite_available,
        analysis=analysis,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    app.run(debug=True)
