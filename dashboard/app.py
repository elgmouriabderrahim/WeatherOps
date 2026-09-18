import streamlit as st
from getdata import df

st.title("WeatherOps Dashboard")
st.write("displaying weather data and analysis.")


city_count = df["city_name"].nunique()
max_temperature = df["temperature_max_c"].max()
min_temperature = df["temperature_min_c"].min()
max_precipitation = df["precipitation_mm"].max()
risky_periods = df[df["risk_level"].isin(["high", "critical"])].shape[0]

highest_risk_city = df.query("risk_score == risk_score.max()")["city_name"].iloc[0]

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 2])

col1.metric("Number of Cities", city_count)
col2.metric("Max Temperature", f"{max_temperature} °C")
col3.metric("Min Temperature", f"{min_temperature} °C")
col4.metric("Max Precipitation", f"{max_precipitation} mm")
col5.metric("Risky Periods", risky_periods)
col6.metric("Highest Risk City", highest_risk_city)