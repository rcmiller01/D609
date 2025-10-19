
CREATE EXTERNAL TABLE IF NOT EXISTS stedi_db.customer_landing (
  customerName string,
  email string,
  phone string,
  birthDay string,
  serialNumber string,
  registrationDate bigint,
  lastUpdateDate bigint,
  shareWithResearchAsOfDate bigint,
  shareWithPublicAsOfDate bigint,
  shareWithFriendsAsOfDate bigint
)
PARTITIONED BY (ingest_date string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://your-bucket/landing/customer/';
