from sqlalchemy import create_engine, text, MetaData, Table, select
from sqlalchemy.dialects.postgresql import insert
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

metadata = MetaData()
weather_table = Table("weather_forecasts",metadata,autoload_with=engine)
cities_table = Table("cities",metadata,autoload_with=engine) 


cities = pd.read_csv('data/silver/clean_cities.csv')
weather = pd.read_csv("data/gold/featured_data.csv")


insert_stmt = insert(cities_table)

city_upsert = insert_stmt.on_conflict_do_nothing(
    index_elements=["city_name", "latitude", "longitude"]
)

with engine.begin() as connection:
    connection.execute(
        city_upsert,
        cities.to_dict(orient="records")
    )


db_cities = pd.read_sql("SELECT id, city_name, latitude, longitude FROM cities", engine)
weather = weather.merge(db_cities, on=["city_name", "latitude", "longitude"], how="left")

weather = weather.rename(columns={
    "id": "city_id",
    "date": "forecast_date"
})

if weather["city_id"].isna().any():
    raise ValueError("Some weather rows could not be matched to cities")

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




insert_stmt = insert(weather_table)

weather_upsert = insert_stmt.on_conflict_do_update(
    index_elements=["city_id", "forecast_date"],
    set_={
        "temperature_max_c": insert_stmt.excluded.temperature_max_c,
        "temperature_min_c": insert_stmt.excluded.temperature_min_c,
        "precipitation_mm": insert_stmt.excluded.precipitation_mm,
        "precipitation_probability_pct": insert_stmt.excluded.precipitation_probability_pct,
        "wind_speed_kmh": insert_stmt.excluded.wind_speed_kmh,
        "wind_gust_kmh": insert_stmt.excluded.wind_gust_kmh,
        "weather_code": insert_stmt.excluded.weather_code,
        "risk_score": insert_stmt.excluded.risk_score,
        "risk_level": insert_stmt.excluded.risk_level,
        "temperature_category": insert_stmt.excluded.temperature_category,
        "precipitation_category": insert_stmt.excluded.precipitation_category,
        "wind_category": insert_stmt.excluded.wind_category,
        "temperature_risk": insert_stmt.excluded.temperature_risk,
        "wind_risk": insert_stmt.excluded.wind_risk,
        "precipitation_risk": insert_stmt.excluded.precipitation_risk,
        "weather_code_risk": insert_stmt.excluded.weather_code_risk,
    }
)

with engine.begin() as connection:
    connection.execute(
        weather_upsert,
        weather.to_dict(orient="records")
    )

