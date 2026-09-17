CREATE TABLE IF NOT EXISTS cities(
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(255) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    UNIQUE(city_name, latitude, longitude)
    );

CREATE TABLE IF NOT EXISTS weather_forecasts(
    id SERIAL PRIMARY KEY,

    city_id INTEGER NOT NULL REFERENCES cities(id),

    forecast_date DATE NOT NULL,

    temperature_max_c DOUBLE PRECISION,
    temperature_min_c DOUBLE PRECISION,

    precipitation_mm DOUBLE PRECISION,
    precipitation_probability_pct INTEGER,

    wind_speed_kmh DOUBLE PRECISION,
    wind_gust_kmh DOUBLE PRECISION,

    weather_code INTEGER,
    weather_code_risk INTEGER,

    temperature_category VARCHAR(50),
    precipitation_category VARCHAR(50),
    wind_category VARCHAR(50),

    temperature_risk INTEGER,
    wind_risk INTEGER,
    precipitation_risk INTEGER,

    risk_score INTEGER,
    risk_level VARCHAR(50),

    UNIQUE(city_id, forecast_date)
    );