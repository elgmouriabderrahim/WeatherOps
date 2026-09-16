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