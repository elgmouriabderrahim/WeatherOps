from database.db import engine
import pandas as pd
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
    w.weather_code,
    w.weather_code_risk,
    w.temperature_category,
    w.precipitation_category,
    w.wind_category,
    w.temperature_risk,
    w.wind_risk,
    w.precipitation_risk,
    w.risk_score,
    w.risk_level
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
"""
df = pd.read_sql(query, engine)