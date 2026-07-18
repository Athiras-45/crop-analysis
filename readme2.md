# Smart Agriculture Advisory System

## Overview

The Smart Agriculture Advisory System is a simple Python project that helps compare current farm conditions with ideal crop conditions stored in a dataset.

The program loads crop information from a CSV file, performs basic data cleaning using Pandas, and provides simple recommendations based on the user's input.

This project is designed for learning basic Python programming and data analysis using Pandas.

---

## Features

- Load crop data from a CSV dataset
- Perform basic dataset cleaning using Pandas
- Search for a crop in the dataset
- Calculate average temperature and humidity
- Compare current farm conditions with ideal conditions
- Display simple recommendations

---

## Technologies Used

- Python 3
- Pandas
- CSV Dataset

---

## Project Structure

```
SmartAgriculture/
│
├── datasets/
│   └── cropdata_updated.csv
│
├── main.py
├── README.md
```

---

## Dataset

The project uses a CSV dataset containing crop information such as:

- Crop Name
- Temperature
- Humidity
- Soil Type
- Moisture Index
- Seedling Stage
- Irrigation Result

---

## Pandas Operations Used

The following Pandas functions are used in this project:

- `read_csv()` – Load the dataset
- `drop_duplicates()` – Remove duplicate records
- `dropna()` – Remove missing values
- `str.strip()` – Remove extra spaces
- `str.lower()` – Convert crop names to lowercase
- `mean()` – Calculate average temperature and humidity
- `mode()` – Find the most common soil type
- DataFrame filtering – Search for a selected crop

---

## How to Run

1. Install Python 3.
2. Install Pandas.

```
pip install pandas
```

3. Place the dataset inside the `datasets` folder.

4. Run the program.

```
python main.py
```

---

## Sample Output

```
SMART AGRICULTURE ADVISORY SYSTEM

Dataset loaded successfully!
Dataset cleaned successfully!

Enter Crop Name: Rice

Ideal Crop Conditions
-------------------------
Average Temperature : 27.8°C
Average Humidity : 81%
Ideal Soil : Clay

Current Temperature: 30
Current Humidity: 75
Current Soil Type: Clay

Analysis
-------------------------
Temperature is Higher than Ideal
Humidity is Lower than Ideal
Soil Type is Suitable

Recommendations
-------------------------
- Increase irrigation.
- Water the crop more frequently.
```

---

## Learning Outcomes

This project helped in understanding:

- Python programming basics
- User input and output
- Conditional statements
- Working with CSV files
- Data cleaning using Pandas
- Filtering and analyzing data
- Generating simple recommendations

---

## Future Improvements

- Add live weather information
- Integrate soil analysis
- Use machine learning for crop prediction
- Build a graphical user interface
- Display charts and reports

---

## Author

Developed as a beginner Python project for learning data analysis using Pandas and implementing a simple Smart Agriculture Advisory System.
