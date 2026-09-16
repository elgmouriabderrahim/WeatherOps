from pathlib import Path
import requests
import pandas as pd
import json

stored_cities = Path("data/bronze/cities.csv")
stored_weather = Path("data/bronze/weather.json")
weather_url = "https://api.open-meteo.com/v1/forecast"


cities = pd.read_csv(stored_cities)

latitudes = ",".join(cities["lat"].astype(str))
longitudes = ",".join(cities["lng"].astype(str))


params = {
    "latitude": latitudes,
    "longitude": longitudes,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "weather_code",
    ],
    "timezone": "auto",
}
try:
    response = requests.get(weather_url, params=params, timeout=30)
    response.raise_for_status()

    weather_data = response.json()

    with open(stored_weather, "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

    print("weather data loaded successfully")

except requests.exceptions.RequestException as e:
    print(f"fetch data error : {e}")

except requests.exceptions.JSONDecodeError as e:
    print(f"invalid JSON response: {e}")

except OSError as e:
    print(f"file write error: {e}")
