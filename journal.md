# Solar Energy Forecasting Research Journal

## Abstract

This research project proposes a spatiotemporal analysis of solar energy data for regions with substantial solar energy development, focusing on either key US states (California, Arizona, Texas, and Nevada) or high-potential areas in the Middle East and South Asia. This study aims to analyze Global Horizontal Irradiance (GHI) from solar radiation datasets (National Solar Radiation Database(NSRDB)) by applying various ML/DL methods (MLP, LSTM, SVR) and forecasting models (ARIMA, SARIMA). I plan on conducting three time-scales (monthly, weekly, and daily) to evaluate which methods work best in different regions and time-scales. The project outcomes would ideally provide further insights into solar energy grid integration and may help identify optimal forecasting strategies for different geographical contexts.

## Project Overview

### Research Objectives
- Analyze solar energy data across different geographical regions
- Compare performance of various ML/DL methods for solar irradiance forecasting
- Evaluate forecasting accuracy across multiple time scales
- Identify optimal forecasting strategies for different geographical contexts

### Methodology
- Data Source: National Solar Radiation Database (NSRDB)
- Target Regions: 
  - US States: California, Arizona, Texas, Nevada
  - Middle East and South Asia regions
- Machine Learning Methods:
  - MLP (Multilayer Perceptron)
  - LSTM (Long Short-Term Memory)
  - SVR (Support Vector Regression)
- Time Series Models:
  - ARIMA
  - SARIMA
- Time Scales:
  - Monthly
  - Weekly
  - Daily

### Expected Outcomes
- Comparative analysis of forecasting methods across different regions
- Insights into solar energy grid integration
- Recommendations for optimal forecasting strategies based on geographical context
- Understanding of temporal patterns in solar irradiance across different time scales

## Progress Tracking

### [4/20] - Project Initiation
- Created project repository
- Defined research objectives and methodology
- Set up initial project structure

### [4/21] - Data Collection and Initial Setup
- Downloaded NSRDB data for multiple cities across four states:
  - California: Los Angeles (LA), Sacramento (SAC), Redding, Fresno
  - Nevada: Las Vegas, Reno, Elko
  - Texas: Houston, Dallas, San Antonio, Lubbock
  - Arizona: Phoenix, Tucson, Flagstaff
- Set up Python environment with required dependencies
- Created initial project structure with preprocessing and model scripts

### [4/22] - Data Preprocessing Implementation
- Implemented data preprocessing pipeline for NSRDB data
- Created functions for:
  - Loading and combining multiple CSV files
  - Handling metadata rows in NSRDB files
  - Creating datetime index
  - Filtering for daytime hours (6 AM to 6 PM)
  - Handling missing values
  - Creating time-based features (hour and day cyclical encoding)
  - Creating lag features and rolling means for GHI
  - Normalizing numeric features

#### Challenges Faced and Solutions:
1. **Metadata Handling**: NSRDB files contain metadata rows that needed to be skipped
   - Solution: Modified CSV reading to skip first 2 rows

2. **Duplicate Indices**: When combining data from multiple cities, we encountered duplicate datetime indices
   - Solution: Created a multi-index with both Date and City to ensure uniqueness

3. **Time Filtering**: Had issues with time filtering due to index structure
   - Solution: Implemented time filtering before creating the multi-index

4. **Data Integration**: Needed to combine data from multiple cities while preserving city-specific patterns
   - Solution: Added city as a feature and created lag/rolling features grouped by city

### [4/23] - LSTM Model Implementation
- Implemented a Long Short-Term Memory (LSTM) neural network for solar irradiance forecasting
- Model Architecture:
  - Input Layer: Takes sequences of 24 hours of data
  - First LSTM Layer: 64 units with return sequences
  - Dropout Layer: 20% dropout for regularization
  - Second LSTM Layer: 32 units
  - Dropout Layer: 20% dropout
  - Dense Layer: 16 units with ReLU activation
  - Output Layer: Single unit for GHI prediction
- Key Features:
  - Sequence Creation: Converts time series data into overlapping sequences
  - Data Normalization: StandardScaler for feature normalization
  - Validation Split: 20% of training data for validation
  - Early Stopping: Prevents overfitting
  - Metrics: Mean Squared Error (MSE) and Mean Absolute Error (MAE)
- Visualization:
  - Training/Validation loss plots
  - Actual vs. Predicted GHI plots

### [Today] - Model Evaluation and New Experiments
- Evaluated and compared multiple models for solar irradiance forecasting:
  - **Linear Regression**: Achieved MAE = 0.01, RMSE = 0.02, R² = 0.923
  - **LSTM**: Achieved MAE = 0.01, RMSE = 0.02, R² = 0.928
  - **ARIMA**: Achieved MAE = 0.08, RMSE = 0.10, R² = -1.774
- Explored additional modeling options:
  - Planned to implement SARIMA (Seasonal ARIMA) for capturing seasonality in solar data.
  - Outlined and prepared a 1D CNN (Convolutional Neural Network) model from scratch for time series forecasting.
- Next Steps:
- [x] Evaluated and compared ARIMA, Linear Regression and LSTM models (with MAE, RMSE, and R²)
- [x] Added R² as an additional evaluation metric
- [ ] Implement SARIMA (Seasonal ARIMA) model
- [ ] Implement 1D CNN (Convolutional Neural Network) model
- [ ] Continue comparative analysis across all models
- [ ] Visualize and document results for all approaches 