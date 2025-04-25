import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import glob
import os

def preprocess_data(city_path):
    """
    Preprocess solar irradiance data for a specific city.
    
    Args:
        city_path (str): Path to the city's data directory
    
    Returns:
        pd.DataFrame: Preprocessed data
    """
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(city_path) if f.endswith('.csv') and not f.startswith('combined_') and not f.startswith('preprocessed_')]
    
    # Read and combine all files
    dfs = []
    for file in csv_files:
        # Skip the first 2 rows (metadata) and read the data
        df = pd.read_csv(os.path.join(city_path, file), skiprows=2)
        # Add city name as a feature
        df['City'] = os.path.basename(city_path)
        dfs.append(df)
    
    # Combine all dataframes
    df = pd.concat(dfs, ignore_index=True)
    
    return df

def main():
    # Process each city that exists
    cities = ['California/LA', 'California/SAC', 'California/Redding', 'California/Fresno']
    all_data = []
    
    for city in cities:
        if os.path.exists(city):
            print(f"Processing {city}...")
            df = preprocess_data(city)
            all_data.append(df)
        else:
            print(f"Skipping {city} - directory not found")
    
    # Combine all cities' data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Create datetime column first
        combined_df['Date'] = pd.to_datetime(combined_df[['Year', 'Month', 'Day', 'Hour', 'Minute']])
        
        # Filter for daytime hours (6 AM to 6 PM)
        combined_df = combined_df.set_index('Date')
        combined_df = combined_df.between_time('06:00', '18:00')
        combined_df = combined_df.reset_index()
        
        # Now create the multi-index
        combined_df.set_index(['Date', 'City'], inplace=True)
        
        # Handle missing values
        combined_df = combined_df.fillna(method='ffill')  # Forward fill
        combined_df = combined_df.fillna(method='bfill')  # Backward fill for any remaining NaNs
        
        # Create time-based features
        combined_df['Hour_sin'] = np.sin(2 * np.pi * combined_df.index.get_level_values('Date').hour / 24)
        combined_df['Hour_cos'] = np.cos(2 * np.pi * combined_df.index.get_level_values('Date').hour / 24)
        combined_df['Day_sin'] = np.sin(2 * np.pi * combined_df.index.get_level_values('Date').dayofyear / 365)
        combined_df['Day_cos'] = np.cos(2 * np.pi * combined_df.index.get_level_values('Date').dayofyear / 365)
        
        # Create lag features for GHI
        combined_df['GHI_lag_1'] = combined_df.groupby('City')['GHI'].shift(1)
        combined_df['GHI_lag_2'] = combined_df.groupby('City')['GHI'].shift(2)
        combined_df['GHI_lag_3'] = combined_df.groupby('City')['GHI'].shift(3)
        
        # Create rolling mean features
        combined_df['GHI_rolling_mean_3'] = combined_df.groupby('City')['GHI'].rolling(window=3).mean()
        combined_df['GHI_rolling_mean_6'] = combined_df.groupby('City')['GHI'].rolling(window=6).mean()
        
        # Drop rows with NaN values (from lag features)
        combined_df = combined_df.dropna()
        
        # Normalize features
        scaler = MinMaxScaler()
        numeric_cols = ['Temperature', 'DHI', 'DNI', 'GHI', 'GHI_lag_1', 'GHI_lag_2', 
                       'GHI_lag_3', 'GHI_rolling_mean_3', 'GHI_rolling_mean_6']
        combined_df[numeric_cols] = scaler.fit_transform(combined_df[numeric_cols])
        
        # Reset index to make Date and City regular columns
        combined_df = combined_df.reset_index()
        
        # Create output directory if it doesn't exist
        os.makedirs('California', exist_ok=True)
        
        # Save combined preprocessed data
        output_path = 'California/combined_preprocessed_data.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"Saved combined preprocessed data to {output_path}")
        
        # Print some statistics
        print("\nDataset Statistics:")
        print(f"Total number of samples: {len(combined_df)}")
        print("\nSamples per city:")
        print(combined_df['City'].value_counts())
        print("\nDate range:")
        print(f"Start: {combined_df['Date'].min()}")
        print(f"End: {combined_df['Date'].max()}")
    else:
        print("No data was processed!")

if __name__ == "__main__":
    main() 