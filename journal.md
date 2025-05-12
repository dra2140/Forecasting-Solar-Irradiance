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

### [4/24] - Model Evaluation and New Experiments
- Evaluated and compared multiple models for solar irradiance forecasting:
  - **Linear Regression**: Achieved MAE = 0.01, RMSE = 0.02, R² = 0.923
  - **LSTM**: Achieved MAE = 0.01, RMSE = 0.02, R² = 0.928
  - **ARIMA**: Achieved MAE = 0.08, RMSE = 0.10, R² = -1.774
- Explored additional modeling options:
  - Planned to implement SARIMA (Seasonal ARIMA) for capturing seasonality in solar data.
  - Outlined and prepared a 1D CNN (Convolutional Neural Network) model from scratch for time series forecasting.

### [4/25-4/28] - Expansion, Model Testing, and Project Pivot
- I initially expanded my analysis to 14 cities across California, Texas, Arizona, and Nevada, aiming to capture a wide range of climatic and geographic diversity. My thinking was that a broader dataset would allow for a more robust comparison of forecasting models and reveal how local weather patterns affect solar irradiance predictions.
- I carefully selected cities to represent different climate zones: coastal, desert, valley, and high plains. This included cities like Los Angeles, Sacramento, Redding, Fresno, Las Vegas, Reno, Elko, Houston, Dallas, San Antonio, Lubbock, Phoenix, Tucson, and Flagstaff.
- I preprocessed the data for all 14 cities, applying the same pipeline: filtering for daylight hours, handling missing values, creating time-based and lag features, and normalizing the data. I made sure to keep city as a feature to preserve local patterns.
- My initial plan was to run all models across all 14 cities, but for my rpesenation I only showed the modeling pipeline on two cities—Fresno and Los Angeles—because they represent two very different climates within California (inland valley vs. coastal urban).
- I implemented and compared several models for these two cities: Persistence (baseline), SARIMA, Random Forest, XGBoost, SVR, LSTM, and a hybrid SARIMA-RF model. I evaluated each model using RMSE, MAE, and R², and visualized both learning curves and actual vs. predicted GHI.
- The results showed that in Fresno, SARIMA performed best for monthly forecasts, while LSTM and Random Forest excelled for daily and weekly predictions, especially during periods of high variability. In Los Angeles, all models struggled more due to the marine layer and variable cloud cover, but LSTM and Random Forest still outperformed SARIMA for daily/weekly forecasts.
- Key findings:
  - Machine learning models (Random Forest, XGBoost) consistently outperformed time series models, especially in Fresno, with R² values above 0.97 across all time scales.
  - Los Angeles models showed lower accuracy and higher variability, with R² values ranging from 0.88 to 0.94, reflecting the impact of coastal microclimate and marine layer effects.
  - Feature importance analysis revealed Fresno's forecasts are dominated by Clearsky GHI, while LA's models rely more on cloud type and humidity.
  - Seasonal error analysis showed Fresno's models perform consistently year-round, while LA exhibits greater error in spring and more irregular seasonal patterns.
- Developed concise slide content and scripts for presenting these results, emphasizing the importance of location-specific modeling and the operational implications for grid integration.
- Refined limitations and next steps, linking current challenges (e.g., dependence on Clearsky GHI, lack of air quality data) to future research directions (expanding to more cities, testing alternative features, incorporating AQI/PM2.5, and developing real-time pipelines).
- Reflected on the value of combining quantitative results with clear visual storytelling to communicate findings effectively in a limited presentation timeframe.
- Based on these findings, I reflected on the trade-off between breadth and depth. I realized that running all models on all 14 cities would be impractical and might dilute the quality of my analysis. I decided to pivot: focus on a smaller subset of cities for in-depth modeling and interpretation, while using the broader dataset for exploratory analysis and context.
- My overall plan going forward is to use the insights from Fresno and LA to refine my modeling approach, then selectively apply it to a few more cities that represent distinct climate types.

### [5/1-5/5] - Project Pivot and Presentation Development
- I decided to pivot my project from analyzing 14 cities to focusing on a strategic selection of cities across distinct microclimates in the American Sunbelt
- I selected eight representative cities across four distinct microclimate categories: coastal (Los Angeles, San Francisco), desert (Phoenix, El Paso), mountainous (Denver, Salt Lake City), and subtropical (Atlanta, Miami). This selection was based on their diverse climate characteristics and growing solar energy markets, allowing for meaningful comparison of model performance across different environmental contexts.
-Developed comprehensive feature selection approach:
  * Initial correlation matrix analysis
  * Removed features highly correlated with GHI (DNI, DHI) to prevent data leakage
  * Implemented VIF-based approach for multicollinearity reduction
  * Final feature set organized into three categories:
    - Temporal: Day_cos, Day_sin
    - Solar: Solar Zenith Angle, Cloud Type
    - Meteorological: Dew Point, Wind Speed
- Implemented diverse modeling approaches:
  * Baseline: Persistence model
  * Time Series: ARIMAX and SARIMAX
  * Machine Learning: Random Forest (100 trees), XGBoost (100 trees, lr=0.1, max_depth=5)
  * Deep Learning: LSTM (64→32 neurons, 100 epochs, Adam optimizer, MSE loss)
- Key findings from model evaluation:
  * All locations showed dramatic performance improvements at longer time scales
  * Tree-based models dominated daily/weekly scales
  * Time series models excelled at monthly forecasting
  * Feature importance analysis revealed:
    - Solar Zenith Angle dominated short-term forecasting in most locations
    - Cloud Type was most important in Atlanta's daily forecasting
    - Denver showed consistent reliance on Solar Zenith Angle
- Nnext steps:
  * Cross-validate within microclimates
  * Optimize feature selection for each model type
  * Develop hybrid models combining tree-based and statistical approaches
  * Implement time series cross-validation with rolling windows

### [5/6-5/11] - Final Model Improvements and Cross-Validation
- I implemented time series cross-validation as suggestes by Alp across all models to ensure robust performance evaluation. Results largely confirmed the test set findings, with some insights:
  * Desert regions (Phoenix, El Paso) showed the lowest variance (±0.6-1.2 RMSE)
  * Subtropical locations (Atlanta, Miami) exhibited the highest variance (±2.5-4.1 RMSE)
  * Daily forecast accuracy was consistently validated with cross-validation means typically within 1-2 RMSE points of test results
  * Notable exceptions included Denver's monthly ARIMAX results, where cross-validation showed significantly higher RMSE (19.0±4.2) compared to test performance (7.64)

- Improvmenst to LSTM model arch:
  * Increased epochs from 50 to 400 to allow for more thorough training
  * Implemented early stopping with a patience of 20 epochs to prevent overfitting








