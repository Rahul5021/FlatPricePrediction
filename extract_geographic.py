import pandas as pd
from opencage.geocoder import OpenCageGeocode
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Function to geocode a location using OpenCage Geocoding API
def get_lat_long(location, api_key):
    geocoder = OpenCageGeocode(api_key)
    result = geocoder.geocode(location)
    
    if result:
        # Get the latitude and longitude from the first result
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        return lat, lng
    else:
        # Return None if no result is found
        return None, None

# Load your dataset (adjust the path to your file)
data = pd.read_csv('D:\Data Science\Projects\FlatPricePrediction\data\clean.csv')  # Adjust path as needed

# Extract unique locations (assuming 'location' is the column containing location names)
locations = data['Location'].unique()

# Set your OpenCage API key (replace with your actual API key)
api_key = os.getenv('OPENCAGE_API_KEY')

# Dictionary to store latitudes and longitudes for each location
location_coords = {}

# Loop through each unique location, get its latitude and longitude, and store it
for location in locations:
    if location not in location_coords:
        lat, lng = get_lat_long(location, api_key)
        location_coords[location] = (lat, lng)
        
    # Sleep for a short period to avoid exceeding API request limits
    time.sleep(1)  # Adjust sleep time if needed

# Add latitude and longitude columns to the original dataset
data['latitude'] = data['Location'].map(lambda x: location_coords.get(x, (None, None))[0])
data['longitude'] = data['Location'].map(lambda x: location_coords.get(x, (None, None))[1])

# Save the updated DataFrame to a new CSV file
data.to_csv('D:\Data Science\Projects\FlatPricePrediction\data\clean.csv', index=False)

print("Geocoding complete and coordinates added to the dataset.")
