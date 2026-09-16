import pandas as pd
import json

cities = pd.read_csv("data/bronze/cities.csv")

with open("data/bronze/weather.json", "r", encoding="utf-8") as f:
    weather = json.load(f)


