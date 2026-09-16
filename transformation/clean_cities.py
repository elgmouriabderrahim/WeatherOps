import pandas as pd
import json

cities = pd.read_csv("data/bronze/cities.csv")

with open("data/bronze/weather.json", "r", encoding="utf-8") as f:
    weather = json.load(f)

cities = cities.rename(columns={"city": "city_name", "lat": "latitude", "lng": "longitude"})

weather_df = []
for forecast in weather:
    df = pd.DataFrame(forecast["daily"])
    df["latitude"] = forecast["latitude"]
    df["longitude"] = forecast["longitude"]

    weather_df.append(df)

weather_df = pd.concat(weather_df, ignore_index=True)
weather_df = weather_df.rename(columns={"time": "date", "temperature_2m_max": "temperature_max", "temperature_2m_min": "temperature_min", "precipitation_sum": "precipitation", "precipitation_probability_max": "precipitation_probability", "wind_speed_10m_max": "wind_speed", "wind_gusts_10m_max": "wind_gust"})

print(weather_df)
