import os
import requests
from dotenv  import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_coordinates(city : str):
    url = "https://api.geoapify.com/v1/geocode/search"
    params= {
        "text" : city,
        "apiKey" : API_KEY
    }
    response = requests.get(url,params = params)
    data = response.json()

    if not data["features"]:
        return None
    
    coords = data["features"][0]["geometry"]["coordinates"]

    return coords[1], coords[0]




def get_travel_info(current : str, destination : str):
    start = get_coordinates(current)
    end = get_coordinates(destination)

    if not start or not end:
        return None
    
    url  = "https://api.geoapify.com/v1/routing"

    params = {
        "waypoints": f"{start[0]},{start[1]}|{end[0]},{end[1]}",
        "mode": "drive",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    route = data["features"][0]["properties"]

    distance_km = round(route["distance"] / 1000, 2)
    time_minutes = round(route["time"] / 60)

    return {
        "distance": f"{distance_km} km",
        "travel_time": f"{time_minutes} mins"
    }
