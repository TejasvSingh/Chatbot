import requests
import json
import time  # To handle request pacing for pagination

# Google Maps API key
api_key = "AIzaSyBzuVA4nnafVaR7bjPYZOAlKdKwb2m6b0I"

# Coordinates for the campus center (e.g., TAMUCC)
campus_lat, campus_lng = 27.7079, -97.3248  # Update with accurate coordinates
radius = 1000  # Radius in meters to cover the campus area

# List of place types to search for
place_types = ["university", "library", "restaurant", "cafe", "dormitory", "office", "school"]

# Initialize an empty list to store all campus locations
campus_locations = []

# Loop through each place type and perform the search
for place_type in place_types:
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={campus_lat},{campus_lng}&radius={radius}&type={place_type}&key={api_key}"
    
    while True:
        # Send request to Google Places API
        response = requests.get(url)
        places_data = response.json()

        # Extract relevant information from each result
        for place in places_data.get("results", []):
            location_info = {
                "name": place.get("name"),
                "address": place.get("vicinity", "N/A"),
                "coordinates": {
                    "lat": place["geometry"]["location"]["lat"],
                    "lng": place["geometry"]["location"]["lng"]
                },
                "type": place_type
            }
            campus_locations.append(location_info)

        # Check if there's a next page of results
        next_page_token = places_data.get("next_page_token")
        if next_page_token:
            # Wait a bit before requesting the next page
            time.sleep(2)
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"
        else:
            break  # No more pages, move to the next place type

# Save the results to a JSON file
with open("campus_locations.json", "w") as json_file:
    json.dump(campus_locations, json_file, indent=4)

print("Campus location data saved to campus_locations.json")
