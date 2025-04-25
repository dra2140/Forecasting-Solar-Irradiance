import os
import pandas as pd
import glob

def combine_city_csvs(city_path):
    # Get all CSV files in the city directory
    csv_files = glob.glob(os.path.join(city_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {city_path}")
        return
    
    # Create an empty list to store dataframes
    dfs = []
    
    # Read each CSV file and add a Year column
    for file in csv_files:
        year = os.path.basename(file).split('_')[-1].split('.')[0]
        df = pd.read_csv(file)
        df['Year'] = year
        dfs.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Save the combined dataframe
    output_file = os.path.join(city_path, "combined_data.csv")
    combined_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")

def process_state(state_dir):
    # Get all city directories in the state
    city_dirs = [d for d in os.listdir(state_dir) if os.path.isdir(os.path.join(state_dir, d))]
    
    for city in city_dirs:
        city_path = os.path.join(state_dir, city)
        print(f"Processing {city}...")
        combine_city_csvs(city_path)

def main():
    states = ['California', 'Nevada', 'Arizona', 'Texas']
    
    for state in states:
        print(f"\nProcessing {state}...")
        process_state(state)

if __name__ == "__main__":
    main() 