
# Submission README
# STEDI Human Balance Analytics – Landing → Trusted → Curated

## Setup
- Region: us-east-1
- Athena workgroup: stedi-wg (Output: s3://<bucket>/athena-results/)
- Database: stedi
- S3 prefixes:
  - customer/landing/, accelerometer/landing/, step_trainer/landing/
  - customer/trusted/, accelerometer/trusted/, step_trainer/trusted/
  - customer/curated/, machine_learning/curated/

## Landing Tables (Athena SQL in repo)
- customer_landing.sql
- accelerometer_landing.sql
- step_trainer_landing.sql

## Glue Jobs (SQL joins, Parquet/Snappy)
Run order:
1. customer_landing_to_trusted → customer_trusted (482)
2. accelerometer_landing_to_trusted → accelerometer_trusted (40981)
3. customers_trusted_to_curated → customers_curated (482)
4. step_trainer_landing_to_trusted → step_trainer_trusted (14460)
5. build_machine_learning_curated → machine_learning_curated (43681)

## Screenshots
- customer_landing.png
- accelerometer_landing.png
- step_trainer_landing.png
- customer_trusted.png

## Verification Queries
(Counts listed above; see Athena section.)
