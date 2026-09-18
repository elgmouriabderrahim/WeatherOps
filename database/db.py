from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")

db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)