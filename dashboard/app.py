import streamlit as st
import pandas as pd
from database.db import engine

st.title("WeatherOps Dashboard")


query = """
SELECT
    c.city_name,
    c.latitude,
    c.longitude,
    w.forecast_date,
    w.temperature_max_c,
    w.temperature_min_c,
    w.precipitation_mm,
    w.precipitation_probability_pct,
    w.wind_speed_kmh,
    w.wind_gust_kmh,
    w.risk_score,
    w.risk_level
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
"""


df = pd.read_sql(query, engine)


st.dataframe(df)