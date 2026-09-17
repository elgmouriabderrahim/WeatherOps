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