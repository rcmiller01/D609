# AWS Configuration Template

## S3 Bucket Configuration
Replace `your-bucket` with your actual S3 bucket name in these files:
- `src/config.py`
- `glue_job_settings.json`
- All SQL DDL files in `sql/landing_ddls/`

## Required S3 Bucket Structure
```
your-bucket/
├── landing/
│   ├── customer/
│   ├── accelerometer/
│   └── step_trainer/
├── trusted/
│   ├── customer/
│   ├── accelerometer/
│   └── step_trainer/
└── curated/
    ├── customer/
    └── ml_ready/
```

## Example Bucket Names to Use
- Production: `stedi-lake-house-your-initials` (e.g., `stedi-lake-house-rm`)
- Development: `stedi-lake-house-dev-your-initials`

## Glue Database
- Database name: `stedi_db` (already configured)

## Job Execution Order
1. `customer_landing_to_trusted`
2. `accelerometer_landing_to_trusted` (depends on #1)
3. `step_trainer_landing_to_trusted`
4. `customer_trusted_to_curated` (depends on #1, #2)
5. `step_trainer_trusted_curated_join` (depends on #3, #4)
6. `machine_learning_curated` (depends on #2, #4, #5)

## Next Steps
1. Create S3 bucket with proper structure
2. Upload data to landing zones
3. Update bucket names in config files
4. Create Glue database
5. Run DDL scripts to create tables
6. Execute Glue jobs in order
7. Validate with Athena queries