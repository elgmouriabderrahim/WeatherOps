SELECT
    c.city_name,
    MAX(w.temperature_max_c) AS max_temperature_c
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.city_name
ORDER BY max_temperature_c DESC;

SELECT
    c.city_name,
    MAX(w.precipitation_mm) AS max_precipitation_mm
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.city_name
ORDER BY max_precipitation_mm DESC;


SELECT
    c.city_name,
    AVG(w.risk_score) AS average_risk_score
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.city_name
ORDER BY average_risk_score DESC;


SELECT
    w.forecast_date,
    MAX(w.risk_score) AS max_risk_score
FROM weather_forecasts w
GROUP BY w.forecast_date
ORDER BY max_risk_score DESC;


SELECT
    c.city_name,
    w.forecast_date,
    w.risk_score
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
WHERE w.risk_score = (
    SELECT MAX(w2.risk_score)
    FROM weather_forecasts w2
    WHERE w2.city_id = w.city_id
)
ORDER BY w.risk_score DESC;


SELECT
    c.city_name,
    w.forecast_date,
    w.risk_score,
    RANK() OVER (
        PARTITION BY c.city_name
        ORDER BY w.risk_score DESC
    ) AS risk_rank
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id;