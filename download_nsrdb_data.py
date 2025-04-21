import requests
import pandas as pd
import io
import time
import os
import urllib.parse

# Your API key from NREL
API_KEY = "tFbCRRkNV9ztCtcnSB0AcF7F38ENPEJPD8eX81zi"
EMAIL = "diaadem@gmail.com"
BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.json?"

# Define locations with their NSRDB location IDs
locations = {
    "California": [
        {"id": "137337", "name": "Los_Angeles"},
        {"id": "137338", "name": "San_Francisco"},
        {"id": "137339", "name": "San_Diego"},
        {"id": "137340", "name": "Sacramento"},
        {"id": "137341", "name": "Fresno"},
        {"id": "137342", "name": "Long_Beach"},
        {"id": "137343", "name": "Merced"},
        {"id": "137344", "name": "Redding"},
    ],
    "Texas": [
        {"id": "137345", "name": "Houston"},
        {"id": "137346", "name": "Dallas"},
        {"id": "137347", "name": "Austin"},
        {"id": "137348", "name": "San_Antonio"},
        {"id": "137349", "name": "El_Paso"},
        {"id": "137350", "name": "Lubbock"},
        {"id": "137351", "name": "Corpus_Christi"},
        {"id": "137352", "name": "Tyler"},
    ],
    "Arizona": [
        {"id": "137353", "name": "Phoenix"},
        {"id": "137354", "name": "Tucson"},
        {"id": "137355", "name": "Flagstaff"},
        {"id": "137356", "name": "Mesa"},
        {"id": "137357", "name": "Chandler"},
        {"id": "137358", "name": "Prescott"},
        {"id": "137359", "name": "Sierra_Vista"},
        {"id": "137360", "name": "Kingman"},
    ],
    "Nevada": [
        {"id": "137361", "name": "Las_Vegas"},
        {"id": "137362", "name": "Reno"},
        {"id": "137363", "name": "North_Las_Vegas"},
        {"id": "137364", "name": "Henderson"},
        {"id": "137365", "name": "Sparks"},
        {"id": "137366", "name": "Carson_City"},
        {"id": "137367", "name": "South_Lake_Tahoe"},
        {"id": "137368", "name": "Elko"},
    ]
}

def verify_api_key():
    """Verify if the API key is valid"""
    test_url = f"https://developer.nrel.gov/api/nsrdb/v2/solar/status?api_key={API_KEY}"
    try:
        response = requests.get(test_url)
        if response.status_code == 200:
            print("API key is valid!")
            return True
        else:
            print(f"API key verification failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error verifying API key: {str(e)}")
        return False

def get_response_json_and_handle_errors(response: requests.Response) -> dict:
    """Takes the given response and handles any errors, along with providing
    the resulting json

    Parameters
    ----------
    response : requests.Response
        The response object

    Returns
    -------
    dict
        The resulting json
    """
    if response.status_code != 200:
        print(f"An error has occurred with the server or the request. The request response code/status: {response.status_code} {response.reason}")
        print(f"The response body: {response.text}")
        return None

    try:
        response_json = response.json()
    except:
        print(f"The response couldn't be parsed as JSON, likely an issue with the server, here is the text: {response.text}")
        return None

    if 'errors' in response_json and len(response_json['errors']) > 0:
        errors = '\n'.join(response_json['errors'])
        print(f"The request errored out, here are the errors: {errors}")
        return None
    return response_json

def download_data(url, output_file):
    """Download data from the given URL and save it to the output file"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df.to_csv(output_file, index=False)
            print(f"Successfully saved {output_file}")
            return True
        else:
            print(f"Error downloading data: {response.status_code}")
            return False
    except Exception as e:
        print(f"Exception occurred while downloading data: {str(e)}")
        return False

def main():
    # Verify API key before proceeding
    if not verify_api_key():
        print("Please check your API key at https://developer.nrel.gov/signup/")
        print("Make sure to:")
        print("1. Sign up for an account")
        print("2. Verify your email")
        print("3. Generate a new API key")
        print("4. Wait a few minutes for the key to become active")
        return

    # Create state folders if they don't exist
    for state in locations.keys():
        os.makedirs(state, exist_ok=True)

    input_data = {
        'attributes': 'air_temperature,clearsky_dhi,clearsky_dni,clearsky_ghi,dhi,dni,ghi,solar_zenith_angle,ozone,wind_direction,wind_speed,relative_humidity,dew_point',
        'interval': '60',
        'include_leap_day': 'true',
        'api_key': API_KEY,
        'email': EMAIL,
    }

    years = [str(year) for year in range(2000, 2024)]

    for state, state_locations in locations.items():
        for location in state_locations:
            location_id = location["id"]
            name = location["name"]
            
            print(f"Processing {state} - {name}...")
            
            for year in years:
                print(f"Processing year: {year}")
                input_data['names'] = [year]
                input_data['location_ids'] = location_id
                
                headers = {
                    'x-api-key': API_KEY
                }
                
                response = requests.post(BASE_URL, json=input_data, headers=headers)
                data = get_response_json_and_handle_errors(response)
                
                if data and 'outputs' in data:
                    download_url = data['outputs']['downloadUrl']
                    print(f"Data can be downloaded from: {download_url}")
                    
                    output_file = os.path.join(state, f"NSRDB_{name}_{year}.csv")
                    if download_data(download_url, output_file):
                        print(f"Successfully processed {name} for {year}")
                    else:
                        print(f"Failed to download data for {name} in {year}")
                
                # Delay to prevent rate limiting
                time.sleep(2)

if __name__ == "__main__":
    main()