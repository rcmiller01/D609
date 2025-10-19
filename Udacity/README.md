
# STEDI Udacity ETL (Landing → Trusted → Curated)

Jobs:
1. customer_landing_to_trusted.py
2. accelerometer_landing_to_trusted.py
3. step_trainer_landing_to_trusted.py
4. customer_trusted_to_curated.py
5. step_trainer_trusted_curated_join.py
6. machine_learning_curated.py

Use `sql/landing_ddls/*.sql` to create landing tables with appropriate types.
Use `sql/athena_validation/rubric_counts.sql` to validate counts per rubric.
Stand-out: accelerometer trusted filters readings on/after consent time.
