from pathlib import Path
import requests


stored_cities = Path("data/bronze/cities.csv")
url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(stored_cities, "wb") as f:
        f.write(response.content)
    print("cities downloaded successfully")
except requests.exceptions.RequestException as e:
    print(f"download Error :{e}")