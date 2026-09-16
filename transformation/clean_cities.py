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
weather_df = weather_df.rename(columns={
    "time": "date",
    "temperature_2m_max": "temperature_max_c",
    "temperature_2m_min": "temperature_min_c",
    "precipitation_sum": "precipitation_mm",
    "precipitation_probability_max": "precipitation_probability_pct",
    "wind_speed_10m_max": "wind_speed_kmh",
    "wind_gusts_10m_max": "wind_gust_kmh",
    "weather_code": "weather_code"
})

cities = cities[["city_name", "latitude", "longitude"]]

cities[["latitude", "longitude"]] = cities[["latitude", "longitude"]].apply(pd.to_numeric, errors="coerce")

weather_df["date"] = pd.to_datetime(weather_df["date"])
numeric_columns = [
    "temperature_max_c",
    "temperature_min_c",
    "precipitation_mm",
    "precipitation_probability_pct",
    "wind_speed_kmh",
    "wind_gust_kmh",
    "weather_code",
    "latitude",
    "longitude",
]
weather_df[numeric_columns] = weather_df[numeric_columns].apply(
    pd.to_numeric,
    errors="coerce"
)
cities = cities.dropna()
weather_df = weather_df.dropna()