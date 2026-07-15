# 🌾 Smart Agriculture Advisory System

A web app that helps farmers decide whether current conditions on their land actually suit the crop they're growing. You enter your farm's location, crop, and soil type, and it pulls in live weather, checks satellite vegetation data (NDVI), compares everything against ideal growing conditions from a crop dataset, and gives you a straightforward report with recommendations.

This started as a command-line Python script and was later rebuilt into a Flask web app so it's actually usable by someone who isn't running it from a terminal.

## What it does

1. You fill in your farm details — name, crop, soil type, location (lat/long), and area.
2. The app looks up the ideal growing conditions for that crop from a dataset of historical crop data.
3. It fetches the current weather at your farm's coordinates using the Open-Meteo API.
4. It pulls the latest Sentinel-2 satellite imagery for your location (via Microsoft's Planetary Computer) and calculates NDVI to gauge vegetation health.
5. It compares your farm's actual conditions against the ideal ones and flags mismatches — temperature, humidity, soil type, moisture.
6. Based on all of that, it generates a list of practical recommendations (irrigate more, check for cold stress, soil amendment needed, etc.).

## Why

Most small-scale advisory tools either need expensive sensors or ask farmers to guess. This uses free, publicly available data (weather + satellite) plus a crop dataset to give a reasonable, data-backed check without any hardware.

## Tech stack

- **Backend:** Python, Flask
- **Data:** pandas (crop dataset lookups)
- **Weather:** [Open-Meteo API](https://open-meteo.com/) (free, no API key needed)
- **Satellite imagery:** [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/) STAC API (Sentinel-2, also free)
- **Frontend:** plain HTML/CSS templates (Jinja2), no JS framework

## Project structure

```
smart-agri-web/
├── app.py                  # Flask routes — form handling, validation, ties everything together
├── dataset.py               # Loads the crop dataset, returns ideal conditions per crop
├── weather.py                # Fetches live weather from Open-Meteo
├── satellite.py              # Fetches Sentinel-2 imagery, computes NDVI + vegetation health
├── soil.py                    # Compares farm soil type vs. ideal soil type
├── analysis.py                # Compares live conditions against dataset averages
├── recommendation.py           # Turns the analysis into human-readable advice
├── datasets/
│   └── cropdata_updated.csv    # Historical crop condition data
├── templates/
│   ├── index.html              # Farm details form
│   └── results.html             # Report page
├── static/
│   └── style.css                 # Styling
└── requirements.txt
```

## Getting started

**1. Clone the repo and set up a virtual environment**

```bash
git clone <your-repo-url>
cd smart-agri-web
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

> Heads up: `rasterio` (used for reading satellite imagery) can be a pain to install on Windows through pip. If it fails, use conda instead:
> `conda install -c conda-forge rasterio`

**3. Run it**

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser and fill in the form.

## Notes on how it behaves

- The satellite lookup queries a live imagery catalog, so it can take a few seconds — that's normal.
- If there's no cloud-free satellite scene available for a location in the last 90 days, the report still generates fine, just without the satellite section (you'll see a note about it).
- Crop and soil type in the form are dropdowns pulled directly from the dataset, so there's no risk of typos breaking the lookup.
- This is running Flask's built-in dev server, which is fine for local use/demos but shouldn't be used as-is in production. Put it behind `gunicorn` or similar if you're deploying it.

## Possible improvements

- Add more crops to the dataset
- Cache satellite/weather results per location to avoid repeat API calls
- Real thermal surface temperature using Landsat instead of the current rough NDVI-based estimate
- Historical trend view instead of a single snapshot

## License

Feel free to use or modify this for learning purposes.