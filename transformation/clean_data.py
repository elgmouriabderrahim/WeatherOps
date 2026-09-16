import pandas as pd
import json

cities = pd.read_csv("data/bronze/cities.csv")
with open("data/bronze/weather.json", "r", encoding="utf-8") as f:
    weather = json.load(f)


cities = cities.rename(columns={"city": "city_name", "lat": "latitude", "lng": "longitude"})
weather_df = []
for i, forecast in enumerate(weather):
    df = pd.DataFrame(forecast["daily"])
    df["latitude"] = cities.loc[i, "latitude"]
    df["longitude"] = cities.loc[i, "longitude"]
    df["city_name"] = cities.loc[i, "city_name"]
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
cities = cities.dropna().drop_duplicates()
weather_df = weather_df.dropna().drop_duplicates(subset=["city_name", "date"])

cities = cities[cities["latitude"].between(-90, 90) & cities["longitude"].between(-180, 180)]
weather_df = weather_df[weather_df["latitude"].between(-90, 90) & weather_df["longitude"].between(-180, 180)]
weather_df = weather_df[(weather_df["precipitation_mm"] >= 0) & (weather_df["precipitation_probability_pct"].between(0, 100)) & (weather_df["wind_speed_kmh"] >= 0) & (weather_df["wind_gust_kmh"] >= 0)]
weather_df = weather_df[weather_df["temperature_max_c"].between(-60, 60) & weather_df["temperature_min_c"].between(-60, 60)]
weather_df = weather_df[weather_df["temperature_max_c"] >= weather_df["temperature_min_c"]]


weather_df.to_csv("data/silver/clean_weather_data.csv", index=False)
cities.to_csv("data/silver/clean_cities.csv", index=False)