CREATE DATABASE IF NOT EXISTS temperatures;

USE temperatures;

DROP TABLE IF EXISTS temps;
CREATE TABLE temps (
	measure_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	temperature FLOAT,
	humidity FLOAT
)
