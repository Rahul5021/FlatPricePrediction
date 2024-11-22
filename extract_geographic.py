import pandas as pd
from opencage.geocoder import OpenCageGeocode
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Function to geocode a location using OpenCage Geocoding API
def get_lat_long_and_state(location, api_key):
    geocoder = OpenCageGeocode(api_key)
    result = geocoder.geocode(location)
    
    if result:
        # Get the latitude, longitude, and state from the result
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        components = result[0].get('components', {})
        state = components.get('state', None)  # Extract the state
        return lat, lng, state
    else:
        # Return None if no result is found
        return None, None, None

# Load your dataset (adjust the path to your file)
data = pd.read_csv('D:\\Data Science\\Projects\\FlatPricePrediction\\data\\clean.csv')  # Adjust path as needed

# Extract unique locations (assuming 'Location' is the column containing location names)
locations = data['Location'].unique()

# Set your OpenCage API key (replace with your actual API key)
api_key = os.getenv('OPENCAGE_API_KEY')

if not api_key:
    raise ValueError("API key not found in .env file.")

# Dictionary to store latitudes, longitudes, and states for each location
location_coords = {}

# Log file to manually check results
with open('geocode_log.txt', 'w') as log_file:
    # Loop through each unique location, get its latitude, longitude, and state, and store it
    for location in locations:
        if location not in location_coords:
            lat, lng, state = get_lat_long_and_state(f"{location}, India", api_key)
            location_coords[location] = {'latitude': lat, 'longitude': lng, 'state': state}
            
            # Log the result for manual verification
            log_file.write(f"{location}: Lat={lat}, Lng={lng}, State={state}\n")
            
        # Sleep for a short period to avoid exceeding API request limits
        time.sleep(1)  # Adjust sleep time if needed

# Add latitude, longitude, and state columns to the original dataset
data['latitude'] = data['Location'].map(lambda x: location_coords.get(x, {}).get('latitude'))
data['longitude'] = data['Location'].map(lambda x: location_coords.get(x, {}).get('longitude'))
data['state'] = data['Location'].map(lambda x: location_coords.get(x, {}).get('state'))

# Save the updated DataFrame to a new CSV file
data.to_csv('data_with_coordinates_and_states.csv', index=False)

print("Geocoding complete. Coordinates and state information added to the dataset.")
