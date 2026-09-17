from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")

db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

with engine.connect() as connection:
    connection.execute(text("select 1"))

print("Database connection successful")


cities = pd.read_csv('data/silver/clean_cities.csv')
cities.to_sql("cities", engine, if_exists="append", index=False)

weather = pd.read_csv("data/gold/featured_data.csv")
db_cities = pd.read_sql("SELECT id, city_name, latitude, longitude FROM cities", engine)
weather = weather.merge(db_cities, on=["city_name", "latitude", "longitude"], how="left")

weather = weather.rename(columns={
    "id": "city_id",
    "date": "forecast_date"
})

weather = weather[[
    "city_id",
    "forecast_date",
    "temperature_max_c",
    "temperature_min_c",
    "precipitation_mm",
    "precipitation_probability_pct",
    "wind_speed_kmh",
    "wind_gust_kmh",
    "weather_code",
    "risk_score",
    "risk_level",
    "temperature_category",
    "precipitation_category",
    "wind_category",
    "temperature_risk",
    "wind_risk",
    "precipitation_risk",
    "weather_code_risk",
]]

weather.to_sql("weather_forecasts", engine, if_exists="append", index=False)