CREATE DATABASE temperatures;

USE temperatures;

DROP TABLE IF EXISTS temps;
CREATE TABLE temps (
	measure_time TIMESTAMP,
	temperature FLOAT
)