
CREATE EXTERNAL TABLE IF NOT EXISTS stedi_db.step_trainer_landing (
  sensorReadingTime bigint,
  serialNumber string,
  distanceFromObject int
)
PARTITIONED BY (ingest_date string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://your-bucket/landing/step_trainer/';
