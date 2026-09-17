SELECT
    c.city_name,
    MAX(w.temperature_max_c) AS max_temperature_c
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.city_name
ORDER BY max_temperature_c DESC;