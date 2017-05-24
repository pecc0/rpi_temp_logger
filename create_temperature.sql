CREATE DATABASE IF NOT EXISTS temperatures;

USE temperatures;

DROP TABLE IF EXISTS temps;
CREATE TABLE temps (
	measure_time DATETIME NOT NULL DEFAULT NOW(),
	temperature FLOAT,
	humidity FLOAT
)