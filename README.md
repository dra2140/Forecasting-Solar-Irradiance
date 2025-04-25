# Solar Energy Forecasting Project

This project implements solar irradiance forecasting using machine learning and deep learning models, analyzing data from multiple cities across California, Nevada, Texas, and Arizona.

## Project Structure

```
src/
├── data/               # Data processing and preprocessing scripts
│   └── preprocess_data.py
├── models/            # Model implementation and training
│   └── solar_forecast.py
├── utils/             # Utility functions and helper scripts
│   └── combine_csvs.py
└── notebooks/         # Jupyter notebooks for analysis and visualization
    └── preprocess_data.ipynb
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Data Preprocessing:
```bash
python src/data/preprocess_data.py
```

2. Model Training:
```bash
python src/models/solar_forecast.py
```

## Data

The project uses data from the National Solar Radiation Database (NSRDB) for multiple cities across:

### California
- Los Angeles (LA)
- Sacramento (SAC)
- Redding
- Fresno

### Nevada
- Las Vegas
- Reno
- Elko

### Texas
- Houston
- Dallas
- San Antonio
- Lubbock

### Arizona
- Phoenix
- Tucson
- Flagstaff

## Models

- LSTM (Long Short-Term Memory) for solar irradiance forecasting
- Additional models to be implemented (MLP, SVR) 