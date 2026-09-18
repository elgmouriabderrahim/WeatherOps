# WeatherOps

WeatherOps collects weather forecasts for Moroccan cities, cleans and enriches them with weather-risk scores, stores the results in PostgreSQL, and displays them in a Streamlit dashboard. An Apache Airflow DAG runs the pipeline daily.


## planification jira

[Voir le board Jira](https://eaofficialbox.atlassian.net/jira/software/projects/WOPS/boards/35?filter=&groupBy=none&atlOrigin=eyJpIjoiMWU5OTFkNzFjYTZiNDRmZmFhMDM3OGI3NjI1YzcwODciLCJwIjoiaiJ9)


## Stack

- **Python, Requests, and pandas** for extraction and transformation.
- **PostgreSQL, SQLAlchemy, and Psycopg** for storage and loading.
- **Apache Airflow** for scheduling.
- **Streamlit and Pydeck** for charts and the weather-risk map.
- **Docker Compose** for running the services locally.

## Data pipeline

```text
City CSV + weather API
        ↓
Bronze: raw city and forecast files
        ↓
Silver: cleaned cities and weather records
        ↓
Gold: weather categories and risk scores
        ↓
PostgreSQL → Streamlit dashboard
```

The pipeline downloads Moroccan city coordinates from SimpleMaps and forecasts from Open-Meteo. Its tasks run in this order:

1. `extract_cities` — download the city CSV.
2. `extract_weather` — request daily weather forecasts for those cities.
3. `silver_transformation` — clean, validate, and deduplicate the data.
4. `gold_feature_engineering` — calculate weather categories and risk scores.
5. `load_postgresql` — insert cities and upsert forecasts by city and forecast date.

The DAG is named `weatherops_pipeline`. It uses an `@daily` schedule, starts on September 18, 2026, and disables historical catchup. Failed tasks have two retries, two minutes apart.

## Run with Docker

### 1. Configure the environment

Install Docker with the Docker Compose plugin. Run the following commands from the project root.

If you do not already have a `.env` file, copy the example:

```bash
cp .env.example .env
```

Edit `.env` with your database settings:

```dotenv
POSTGRES_DB=weatherops
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace_with_your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Compose uses these credentials for PostgreSQL. Inside the dashboard and Airflow containers, it overrides the database host to `postgres` and the port to `5432`. `POSTGRES_PORT` in `.env` controls the port exposed on your host.

### 2. Start the services

```bash
docker compose up --build -d
```

| Service | Address | Purpose |
| --- | --- | --- |
| Dashboard | http://localhost:8501 | Streamlit charts and map |
| Airflow | http://localhost:8080 | Pipeline scheduling and task logs |
| PostgreSQL | `localhost:<POSTGRES_PORT>` | Weather database |

Airflow runs in standalone mode for local development. Its metadata is stored separately from the weather database.

### 3. Load the first forecasts

Check the Airflow startup logs for login details:

```bash
docker compose logs airflow
```

Open Airflow, find `weatherops_pipeline`, unpause it, and trigger a run. Wait for all five tasks to succeed before opening the dashboard on a fresh database: the current dashboard expects forecast rows to exist.

If the dashboard was opened before loading finished, restart it to reload its imported data:

```bash
docker compose restart dashboard
```

## Dashboard

The dashboard includes city counts, temperature and precipitation metrics, risk charts, city-specific weather trends, and a weather-risk map. Filters support city, risk level, a date range, and a specific date.

The map averages each city's temperature, precipitation, wind speed, and risk score across rows matching the selected filters. Its tooltip includes the number of contributing dates. Rainfall on the map is a daily average, not a total for the selected period.

## Risk scoring

The score adds four components:

| Component | Maximum points |
| --- | ---: |
| Maximum daily temperature | 25 |
| Daily precipitation | 30 |
| Wind speed | 30 |
| Weather code | 15 |
| **Total** | **100** |

The scoring rules are defined in `transformation/feature_engineering.py`.

## Project structure

```text
WeatherOps/
├── dags/weather_pipeline.py          # Airflow DAG
├── dashboard/
│   ├── app.py                        # Streamlit dashboard and map
│   └── getdata.py                    # Dashboard database query
├── database/db.py                    # SQLAlchemy connection
├── extraction/
│   ├── extract_cities.py
│   └── extract_weather.py
├── transformation/
│   ├── clean_data.py
│   └── feature_engineering.py
├── load/load_postgres.py             # Database upserts
├── sql/
│   ├── schema.sql                    # Tables and constraints
│   └── analytics.sql                 # Analytical queries
├── data/                             # Local pipeline outputs
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Storage and common commands

Compose keeps data in three named volumes:

- `postgres_data`: weather database.
- `airflow_data`: Airflow metadata and logs.
- `weather_data`: bronze, silver, and gold files under `/app/data` in the Airflow container. These are separate from the host's `data/` directory.

The PostgreSQL schema runs automatically only when its data volume is first initialized. Editing `sql/schema.sql` does not update an existing database automatically.

View service status and logs:

```bash
docker compose ps
docker compose logs -f airflow
docker compose logs -f dashboard
```

Stop the services while retaining their data:

```bash
docker compose down
```

Rebuild after changing Python code, the DAG, or dependencies, since these files are copied into the image:

```bash
docker compose up --build -d
```
