# Solar Energy Forecasting Project

This project implements solar irradiance forecasting using machine learning and deep learning models, analyzing data across different microclimates in the American Sunbelt. The project focuses on evaluating model performance across diverse environmental contexts and time scales.

## Project Structure

```
.
├── src/                    # Source code
│   └── preprocess_data.py  # Data preprocessing pipeline
├── Coastal/               # Coastal microclimate data and results
│   ├── Los_Angeles/
│   └── San_Francisco/
├── Desert/                # Desert microclimate data and results
│   ├── Phoenix/
│   └── El_Paso/
├── Mountainous/           # Mountainous microclimate data and results
│   ├── Denver/
│   └── Salt_Lake_City/
├── Subtropical/           # Subtropical microclimate data and results
│   ├── Atlanta/
│   └── Miami/
├── requirements.txt       # Project dependencies
├── journal.md            # Project development journal
└── abstract.md           # Project abstract
```

## Setup

### Local Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Google Colab Setup
1. Open the project in Google Colab:
   - Upload the project files to your Google Drive
   - Open a new Colab notebook
   - Mount your Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. Set the correct file paths:
   ```python
   # Set base directory to your project folder in Google Drive
   BASE_DIR = '/content/drive/MyDrive/Forecasting-Solar-Irradiance'
   
   # Update paths in preprocess_data.py
   COASTAL_DIR = f'{BASE_DIR}/Coastal'
   DESERT_DIR = f'{BASE_DIR}/Desert'
   MOUNTAINOUS_DIR = f'{BASE_DIR}/Mountainous'
   SUBTROPICAL_DIR = f'{BASE_DIR}/Subtropical'
   ```

3. Install required packages:
   ```python
   !pip install -r requirements.txt
   ```

4. Run the preprocessing script:
   ```python
   %run src/preprocess_data.py
   ```

## Data

The project uses data from the National Solar Radiation Database (NSRDB) for cities across four distinct microclimates:

### Coastal Microclimate
- Los Angeles, CA
- San Francisco, CA

### Desert Microclimate
- Phoenix, AZ
- El Paso, TX

### Mountainous Microclimate
- Denver, CO
- Salt Lake City, UT

### Subtropical Microclimate
- Atlanta, GA
- Miami, FL

## Models

The project implements and evaluates multiple forecasting approaches:

### Time Series Models
- ARIMAX
- SARIMAX

### Machine Learning Models
- Random Forest (100 trees)
- XGBoost (100 trees, learning rate=0.1, max_depth=5)

### Deep Learning Models
- LSTM (64→32 neurons, 400 epochs with early stopping)

## Features

The models use a carefully selected feature set:
- Temporal Features: Day_cos, Day_sin
- Solar Features: Solar Zenith Angle, Cloud Type
- Meteorological Features: Dew Point, Wind Speed

## Results

The project evaluates model performance across three time scales:
- Daily forecasts
- Weekly forecasts
- Monthly forecasts

Key findings include:
- Tree-based models dominate daily/weekly scales
- Time series models excel at monthly forecasting
- Performance varies significantly by microclimate
- Cross-validation confirms model robustness

## Development Journal

The project's development process and key decisions are documented in `journal.md`, including:
- Initial project setup and data collection
- Feature selection methodology
- Model implementation and improvements
- Cross-validation results
- Final performance analysis 