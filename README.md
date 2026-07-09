# crop-analysis
# Smart Agriculture Advisory System

## About the Project

The Smart Agriculture Advisory System is a Python-based project developed to help farmers make better farming decisions by using weather data, agricultural datasets, and satellite information. The system collects farm details from the user, analyzes the current weather conditions, compares them with ideal crop conditions from a dataset, and provides suitable farming recommendations.

The project also includes a Power BI dashboard to visualize agricultural data in an easy-to-understand format.

---

## Objective

To develop a simple smart agriculture system that provides location-based farming recommendations using live weather data, crop dataset analysis, and satellite-based vegetation monitoring.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- Google Earth Engine API
- Open-Meteo API
- Power BI

---

## Project Structure

```
SmartAgriculture/
│
├── datasets/
│   └── smart_agriculture_dataset.csv
│
├── main.py
├── farm.py
├── weather.py
├── dataset.py
├── satellite.py
├── analysis.py
├── recommendation.py
├── utils.py
│
├── requirements.txt
└── README.md
```

---

## Data Sources

### Open-Meteo API

Used to get live weather information such as:

- Temperature
- Humidity
- Rainfall
- Wind Speed
- Pressure

Website:
https://open-meteo.com/

API:
https://api.open-meteo.com/v1/forecast

---

### Smart Agriculture Dataset

Source:
https://www.kaggle.com/datasets/chaitanyagopidesi/smart-agriculture-dataset

The dataset includes:

- Crop Name
- Temperature
- Humidity
- Soil Type
- Moisture Index
- Seedling Stage
- Irrigation Requirement

---

### Google Earth Engine

Used to obtain satellite-based crop information like:

- NDVI
- Vegetation Health

Website:
https://earthengine.google.com/

---

## How the Project Works

1. The user enters farm details.
2. The crop data is loaded from the dataset.
3. Live weather data is fetched using the Open-Meteo API.
4. Satellite information is retrieved using Google Earth Engine.
5. The system compares live weather with the dataset values.
6. Recommendations are generated based on the analysis.
7. The final report is displayed.

---

## Features

- Farm information management
- Live weather retrieval
- Crop dataset analysis
- Satellite-based vegetation analysis
- Farming recommendations
- Power BI dashboard

---

## Power BI Dashboard

The dashboard displays:

- Crop Distribution
- Temperature Analysis
- Humidity Analysis
- Soil Type Distribution
- Moisture Index
- Irrigation Requirement
- Weather Summary
- Crop Health (NDVI)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/SmartAgriculture.git
```

Go to the project folder:

```bash
cd SmartAgriculture
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

## Required Libraries

```
pandas
numpy
requests
rich
earthengine-api
```

---

## Future Improvements

- Add machine learning for crop prediction.
- Detect crop diseases using image processing.
- Develop a mobile application.
- Support multiple languages.
- Connect IoT sensors for real-time monitoring.

---

## Developed By

**Athira S**

St. Xavier Catholic College of Engineering

---

## Note

This project was developed as a college mini project for learning and demonstration purposes.
