import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import glob
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def preprocess_data(data_dir, state_city_path, apply_scaling=False):
    full_path = os.path.join(data_dir, state_city_path)
    csv_files = [f for f in os.listdir(full_path) if f.endswith('.csv') and not f.startswith('combined_') and not f.startswith('preprocessed_')]
    
    dfs = []
    for file in csv_files:
        file_path = os.path.join(full_path, file)
        try:
            df = pd.read_csv(file_path, skiprows=2)
            state, city = state_city_path.split('/')
            df['State'] = state
            df['City'] = city
            dfs.append(df)
            print(f"Successfully read {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        return df
    else:
        print(f"No data found for {state_city_path}")
        return None

def main(apply_scaling=False):
    data_dir = "."  
    
    state_cities = [
        'California/LA',
        'Arizona/Pheonix', 
        'Colorado/Denver',
        'Georgia/Atlanta',
        'Florida/Miami',
        'Texas/El Paso',
        'California/SF',
        'Utah/SLC' ]

    all_data = []
    
    for state_city in state_cities:
        full_path = os.path.join(data_dir, state_city)
        if os.path.exists(full_path):
            print(f"Processing {state_city}...")
            df = preprocess_data(data_dir, state_city)
            if df is not None:
                if 'Year' in df.columns and 'Month' in df.columns and 'Day' in df.columns and 'Hour' in df.columns and 'Minute' in df.columns:
                    df['Date'] = pd.to_datetime(
                        df['Year'].astype(str) +
                        df['Month'].astype(str).str.zfill(2) +
                        df['Day'].astype(str).str.zfill(2) +
                        df['Hour'].astype(str).str.zfill(2) +
                        df['Minute'].astype(str).str.zfill(2),
                        format='%Y%m%d%H%M'
                    )
                    all_data.append(df)
                else:
                    print(f"Warning: Missing date columns in data from {state_city}")
        else:
            print(f"Skipping {state_city} - directory not found: {full_path}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        combined_df = combined_df.set_index('Date')
        combined_df = combined_df.between_time('08:00', '17:00')
        combined_df = combined_df.reset_index()
        
        combined_df.set_index(['Date', 'State', 'City'], inplace=True)
        
        combined_df = combined_df.fillna(method='ffill')
        combined_df = combined_df.fillna(method='bfill')
        
        combined_df['Hour_sin'] = np.sin(2 * np.pi * combined_df.index.get_level_values('Date').hour / 24)
        combined_df['Hour_cos'] = np.cos(2 * np.pi * combined_df.index.get_level_values('Date').hour / 24)
        combined_df['Day_sin'] = np.sin(2 * np.pi * combined_df.index.get_level_values('Date').dayofyear / 365)
        combined_df['Day_cos'] = np.cos(2 * np.pi * combined_df.index.get_level_values('Date').dayofyear / 365)
        
        combined_df['GHI_lag_1'] = combined_df.groupby(['State', 'City'])['GHI'].shift(1)
        combined_df['GHI_lag_2'] = combined_df.groupby(['State', 'City'])['GHI'].shift(2)
        combined_df['GHI_lag_3'] = combined_df.groupby(['State', 'City'])['GHI'].shift(3)
        
        combined_df['GHI_rolling_mean_3'] = combined_df.groupby(['State', 'City'])['GHI'].rolling(window=3).mean().reset_index(level=[0, 1], drop=True)
        combined_df['GHI_rolling_mean_6'] = combined_df.groupby(['State', 'City'])['GHI'].rolling(window=6).mean().reset_index(level=[0, 1], drop=True)
        
        combined_df = combined_df.dropna()
        
        numeric_cols = [
            'Temperature', 'DHI', 'DNI', 'GHI', 
            'Clearsky GHI', 'Solar Zenith Angle', 
            'Cloud Type', 'Relative Humidity', 'Pressure',
            'Precipitable Water', 'Wind Speed', 'Wind Direction',
            'GHI_lag_1', 'GHI_lag_2', 'GHI_lag_3', 
            'GHI_rolling_mean_3', 'GHI_rolling_mean_6'
        ]
        
        numeric_cols = [col for col in numeric_cols if col in combined_df.columns]
        
        unscaled_df = combined_df.copy()
        
        if apply_scaling:
            scaler = MinMaxScaler()
            combined_df[numeric_cols] = scaler.fit_transform(combined_df[numeric_cols])
            scaling_suffix = ''
        else:
            scaling_suffix = '_unscaled'
        
        combined_df = combined_df.reset_index()
        unscaled_df = unscaled_df.reset_index()
        
        for state in combined_df['State'].unique():
            os.makedirs(state, exist_ok=True)
        
        output_path = f'combined_preprocessed_data{scaling_suffix}.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"Saved combined preprocessed data to {output_path}")
        
        if apply_scaling:
            unscaled_df.to_csv('combined_preprocessed_data_unscaled.csv', index=False)
            print(f"Saved unscaled version to combined_preprocessed_data_unscaled.csv")
        
        for state_city_group, group_df in combined_df.groupby(['State', 'City']):
            state, city = state_city_group
            safe_city = city.replace(' ', '_')
            output_file = os.path.join(state, f"preprocessed_{safe_city}{scaling_suffix}.csv")
            group_df.to_csv(output_file, index=False)
            print(f"Saved {state}/{city} data to {output_file}")
            
            if apply_scaling:
                unscaled_group = unscaled_df[(unscaled_df['State'] == state) & (unscaled_df['City'] == city)]
                unscaled_output = os.path.join(state, f"preprocessed_{safe_city}_unscaled.csv")
                unscaled_group.to_csv(unscaled_output, index=False)
        
        print("\nDataset Statistics:")
        print(f"Total number of samples: {len(combined_df)}")
        print("\nSamples per state/city:")
        print(combined_df.groupby(['State', 'City']).size())
        print("\nDate range:")
        print(f"Start: {combined_df['Date'].min()}")
        print(f"End: {combined_df['Date'].max()}")
    else:
        print("No data was processed!")

if __name__ == "__main__":
    apply_scaling = False
    main(apply_scaling)