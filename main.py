import requests
import math
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Original point
lat0, lon0 = 19.392746, -99.172805

# 200m to the south
lat1 = lat0 - (200 / 111_320)
lon1 = lon0

# Find hospitals named "Angeles Hospital" nearby
def search_hospitals(lat, lon, radius=5000, keyword="Hospital Angeles&type=hospital"):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lon}&radius={radius}"
        f"&keyword={keyword}&key={API_KEY}"
    )
    res = requests.get(url)
    return res.json().get("results", [])

# Calculate driving distance from one point to multiple destinations
def get_distances(origin, destinations):
    dest_str = "|".join([f"{d['geometry']['location']['lat']},{d['geometry']['location']['lng']}" for d in destinations])
    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin[0]},{origin[1]}"
        f"&destinations={dest_str}"
        f"&mode=driving&key={API_KEY}"
    )
    res = requests.get(url).json()
    distances = []
    for i, el in enumerate(res["rows"][0]["elements"]):
        if el["status"] == "OK":
            distances.append((destinations[i]["name"], el["distance"]["text"], el["distance"]["value"]))
            # print(distances)
    return sorted(distances, key=lambda x: x[2])

# Find hospitals and calculate distances from the accident site
hospitals = search_hospitals(lat0, lon0)
print(f"Se encontraron {len(hospitals)} Hospitales Angeles en 5 km")

distances = get_distances((lat1, lon1), hospitals)

if distances:
    name, distance_txt, distance_m = distances[0]
    print(f"El hospital más cercano es: {name} ({distance_txt})")
else:
    print("No se encontraron hospitales Angeles cercanos")
