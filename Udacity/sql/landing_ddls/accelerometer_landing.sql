
CREATE EXTERNAL TABLE IF NOT EXISTS stedi_db.accelerometer_landing (
  `user` string,
  timestamp bigint,
  x double,
  y double,
  z double
)
PARTITIONED BY (ingest_date string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://your-bucket/landing/accelerometer/';
