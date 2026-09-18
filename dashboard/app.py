import streamlit as st
from getdata import load_data
import pandas as pd

df = load_data()

st.set_page_config(layout="wide")

if df.empty:
    st.warning("No weather data available.")
    st.stop()


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


with st.sidebar:
    select_city = st.selectbox("Select a city to view its weather data:",["All"] + sorted(df["city_name"].unique()))
    select_risk_level = st.selectbox("Select a risk level to filter the data:", ["All", "low", "moderate", "high", "critical"])
    select_date_range = st.date_input("Select a period:",value=(df["forecast_date"].min(),df["forecast_date"].max()))
    select_date = st.selectbox("Select a specific date:", ["All"] + sorted(df["forecast_date"].unique()))

if select_city == "All":
    filtered_df = df
else:
    filtered_df = df[df["city_name"] == select_city]
if select_risk_level != "All":
    filtered_df = filtered_df[filtered_df["risk_level"] == select_risk_level]
if select_date != "All":
    filtered_df = filtered_df[filtered_df["forecast_date"] == select_date]
if len(select_date_range) == 2:
    start_date, end_date = select_date_range
    filtered_df = filtered_df[
        filtered_df["forecast_date"].between(start_date, end_date)
    ]
if select_date != "All":
    filtered_df = filtered_df[filtered_df["forecast_date"] == select_date]

dashboard_left, dashboard_right = st.columns(2)

with dashboard_left:
    risk_by_city = (filtered_df.groupby("city_name")["risk_score"].mean().sort_values(ascending=False))
    st.subheader("Risk by City")
    st.bar_chart(risk_by_city)



with dashboard_right:
    if select_city != "All":
        weather_over_time = filtered_df.copy()
        weather_over_time["forecast_date"] = weather_over_time["forecast_date"].astype(str)
        weather_over_time = weather_over_time.sort_values("forecast_date").set_index("forecast_date")

        st.subheader(f"Weather Over Time for {select_city}")
        st.line_chart(weather_over_time[["temperature_max_c", "temperature_min_c"]])

        st.subheader(f"Precipitation Over Time for {select_city}")
        st.bar_chart(weather_over_time[["precipitation_mm"]])


import pydeck as pdk

st.subheader("Weather Risk Map")
if filtered_df.empty:
    st.info("No weather data matches the selected filters.")
else:
    map_df = (
        filtered_df.groupby(["city_name", "latitude", "longitude"], as_index=False)
        .agg(
            risk_score=("risk_score", "mean"),
            temperature_max_c=("temperature_max_c", "mean"),
            temperature_min_c=("temperature_min_c", "mean"),
            precipitation_mm=("precipitation_mm", "mean"),
            wind_speed_kmh=("wind_speed_kmh", "mean"),
            days=("forecast_date", "nunique"),
        )
    )
    map_df["risk_level"] = pd.cut(
        map_df["risk_score"],
        bins=[0, 25, 50, 75, 101],
        labels=["low", "moderate", "high", "critical"],
        right=False,
    ).astype(object)
    map_df["color"] = map_df["risk_level"].map({
        "low": [0, 220, 120, 255],
        "moderate": [255, 220, 0, 255],
        "high": [255, 140, 0, 255],
        "critical": [255, 50, 50, 255],
    })
    map_df = map_df.round(2)

    st.caption("Each city shows daily averages across the dates matching your filters. Colors represent average risk.")
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["longitude", "latitude"],
        get_radius="risk_score * 100",
        radius_min_pixels=5,
        get_fill_color="color",
        pickable=True,
    )
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=5,
        ),
        tooltip={"html": """
            <b>{city_name}</b><br>
            Days: {days}<br>
            Avg Risk: {risk_score} ({risk_level})<br>
            Avg Max Temp: {temperature_max_c} °C<br>
            Avg Min Temp: {temperature_min_c} °C<br>
            Avg Daily Rain: {precipitation_mm} mm<br>
            Avg Wind: {wind_speed_kmh} km/h
        """},
    ))


if select_city == "All":
    highest_risk_locations = (filtered_df.groupby("city_name")["risk_score"].max().sort_values(ascending=False).head(10).reset_index())
    st.subheader("Highest Risk Locations")
    st.dataframe(highest_risk_locations, use_container_width=True)