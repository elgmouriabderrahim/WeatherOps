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