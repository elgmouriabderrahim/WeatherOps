import pandas as pd

weather_df = pd.read_csv("data/silver/clean_weather_data.csv")

weather_df["temperature_category"] = pd.cut(
    weather_df["temperature_max_c"],
    bins=[-float("inf"), 10, 25, 35, float("inf")],
    labels=["cold", "normal", "hot", "extreme"]
)

weather_df["precipitation_category"] = pd.cut(
    weather_df["precipitation_mm"],
    bins=[-float("inf"), 0, 5, 20, float("inf")],
    labels=["none", "light", "moderate", "heavy"]
)

weather_df["wind_category"] = pd.cut(
    weather_df["wind_speed_kmh"],
    bins=[-float("inf"), 20, 40, 60, float("inf")],
    labels=["low", "moderate", "strong", "severe"]
)

# Weather Risk Score formula:
# Temperature risk: max 25 points
# Precipitation risk: max 30 points
# Wind risk: max 30 points
# Weather-code risk: max 15 points
# Total risk score: 0–100


temperature_points = {
    "cold": 15,
    "normal": 0,
    "hot": 10,
    "extreme": 25,
}
weather_df["temperature_risk"] = weather_df["temperature_category"].map(temperature_points).astype(int)



precipitation_points = {
    "none": 0,
    "light": 10,
    "moderate": 20,
    "heavy": 30,
}
weather_df["precipitation_risk"] = weather_df["precipitation_category"].map(precipitation_points).astype(int)



wind_points = {
    "low": 0,
    "moderate": 10,
    "strong": 20,
    "severe": 30,
}
weather_df["wind_risk"] = weather_df["wind_category"].map(wind_points).astype(int)


def weather_code_risk(code):
    if code in [0, 1, 2]:
        return 0
    elif code in [3, 45, 48]:
        return 5
    elif 51 <= code <= 82:
        return 10
    elif 85 <= code <= 99:
        return 15
    return 0

weather_df["weather_code_risk"] = weather_df["weather_code"].apply(
    weather_code_risk
)

weather_df["risk_score"] = weather_df["temperature_risk"] + weather_df["precipitation_risk"] + weather_df["wind_risk"] + weather_df["weather_code_risk"]

weather_df["risk_level"] = pd.cut(
    weather_df["risk_score"],
    bins = [-1,25, 50, 75, 100],
    labels=["low", "modurate", "high", "critical"],
    right=False
)