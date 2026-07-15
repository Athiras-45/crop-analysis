"""
satellite.py
-------------
Fetches satellite data using the FREE Microsoft Planetary Computer STAC API.
No client ID / client secret / paid account needed.

Returns:
- NDVI
- Vegetation Health
- Surface Temperature (Estimated)

Requires:
    pip install pystac-client planetary-computer rasterio numpy
"""

import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio.warp import transform_bounds
from pystac_client import Client
import planetary_computer as pc
from datetime import datetime, timedelta

STAC_API_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "sentinel-2-l2a"


def get_satellite_data(latitude, longitude, days_back=90, max_cloud_cover=60):
    """
    Fetch the most recent, low-cloud Sentinel-2 scene covering (lat, lon)
    and compute NDVI + a rough surface temperature estimate.

    Returns a dict, or None if no usable data / a real error occurred.
    """

    try:
        catalog = Client.open(STAC_API_URL, modifier=pc.sign_inplace)

        # Small bbox around the point (~ few hundred meters)
        delta = 0.01
        bbox = [
            longitude - delta,
            latitude - delta,
            longitude + delta,
            latitude + delta,
        ]

        end = datetime.utcnow()
        start = end - timedelta(days=days_back)
        time_range = f"{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}"

        search = catalog.search(
            collections=[COLLECTION],
            bbox=bbox,
            datetime=time_range,
            query={"eo:cloud_cover": {"lt": max_cloud_cover}},
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
        )

        items = list(search.item_collection())

        if not items:
            print(f"No scenes found with <{max_cloud_cover}% cloud cover in the "
                  f"last {days_back} days. Retrying with no cloud filter...")

            fallback_search = catalog.search(
                collections=[COLLECTION],
                bbox=bbox,
                datetime=time_range,
                sortby=[{"field": "properties.datetime", "direction": "desc"}],
            )
            items = list(fallback_search.item_collection())

            if not items:
                print(f"No Sentinel-2 scenes exist AT ALL for ({latitude}, {longitude}) "
                      f"in the last {days_back} days. Double-check your lat/lon order "
                      f"and that this point is over land.")
                return None
            else:
                print(f"Found {len(items)} scene(s) once cloud filter was removed "
                      f"(cloudiest: {max(i.properties.get('eo:cloud_cover', 0) for i in items)}%).")

        item = items[0]  # most recent, already sorted

        red_href = item.assets["B04"].href  # Red band
        nir_href = item.assets["B08"].href  # NIR band

        red = _read_window(red_href, latitude, longitude)
        nir = _read_window(nir_href, latitude, longitude)

        if red is None or nir is None:
            print("Could not read pixel window from imagery.")
            return None

        red = red.astype("float32")
        nir = nir.astype("float32")

        denom = nir + red
        denom[denom == 0] = np.nan
        ndvi_array = (nir - red) / denom

        ndvi = float(np.nanmean(ndvi_array))

        if np.isnan(ndvi):
            print("NDVI computation returned NaN (likely no valid pixels).")
            return None

        # Vegetation classification
        if ndvi < 0.2:
            vegetation = "Very Poor"
        elif ndvi < 0.4:
            vegetation = "Poor"
        elif ndvi < 0.6:
            vegetation = "Moderate"
        elif ndvi < 0.8:
            vegetation = "Healthy"
        else:
            vegetation = "Excellent"

        # Rough approximation only - NOT a real thermal measurement.
        # For real surface temperature, use Landsat 8/9 thermal bands
        # (collection "landsat-c2-l2") instead.
        surface_temperature = round(35 - (ndvi * 8), 2)

        return {
            "NDVI": round(ndvi, 3),
            "Vegetation Health": vegetation,
            "Surface Temperature": surface_temperature,
            "Scene Date": item.properties.get("datetime"),
            "Cloud Cover (%)": item.properties.get("eo:cloud_cover"),
        }

    except Exception as e:
        print("Satellite API Error:", repr(e))
        return None


def _read_window(href, latitude, longitude, pixel_buffer=5):
    """
    Open a Cloud-Optimized GeoTIFF band and read a small window
    of pixels around (latitude, longitude).
    """
    with rasterio.open(href) as src:
        # Reproject the point into the raster's own CRS
        lon_min, lat_min, lon_max, lat_max = transform_bounds(
            "EPSG:4326", src.crs,
            longitude - 0.0001, latitude - 0.0001,
            longitude + 0.0001, latitude + 0.0001,
        )

        row, col = src.index((lon_min + lon_max) / 2, (lat_min + lat_max) / 2)

        row_start = max(row - pixel_buffer, 0)
        col_start = max(col - pixel_buffer, 0)
        window = Window(
            col_start, row_start,
            min(pixel_buffer * 2, src.width - col_start),
            min(pixel_buffer * 2, src.height - row_start),
        )

        data = src.read(1, window=window)
        if data.size == 0:
            return None
        return data
