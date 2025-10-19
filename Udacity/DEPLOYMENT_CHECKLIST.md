# STEDI Project Deployment Checklist

## ✅ Fixes Applied
- [x] Fixed job execution order in `glue_job_settings.json`
- [x] Updated all SQL DDLs to use `stedi_db` database
- [x] Updated validation queries to use `stedi_db`
- [x] Created configuration update script
- [x] Added deployment documentation

## 🚀 Ready for AWS Deployment

### Prerequisites
1. **AWS Account** with Glue, S3, and Athena access
2. **S3 Bucket** created with proper folder structure
3. **Data files** uploaded to landing zones

### Deployment Steps

#### Phase 1: Infrastructure Setup
1. Create S3 bucket (e.g., `stedi-lake-house-rm`)
2. Create folder structure:
   ```
   landing/customer/
   landing/accelerometer/ 
   landing/step_trainer/
   ```
3. Upload provided data files to landing folders
4. Create Glue database: `stedi_db`

#### Phase 2: Configuration Update
1. Run: `python update_config.py --bucket your-bucket-name`
2. Verify all placeholder values are replaced

#### Phase 3: Table Creation
1. Execute DDL scripts in Athena:
   - `sql/landing_ddls/customer_landing.sql`
   - `sql/landing_ddls/accelerometer_landing.sql`
   - `sql/landing_ddls/step_trainer_landing.sql`

#### Phase 4: ETL Execution (In Order!)
1. `customer_landing_to_trusted`
2. `accelerometer_landing_to_trusted`
3. `step_trainer_landing_to_trusted` 
4. `customer_trusted_to_curated`
5. `step_trainer_trusted_curated_join`
6. `machine_learning_curated`

#### Phase 5: Validation
1. Run queries from `sql/athena_validation/rubric_counts.sql`
2. Verify expected counts:
   - Landing: 956 / 81,273 / 28,680
   - Trusted: 482 / 40,981 / 14,460
   - Curated: 482 / 43,681
3. Take screenshots of each table (data + count)

## 🎯 Expected Rubric Results
- ✅ All landing tables with proper JSON schema
- ✅ Privacy filtering (no blank consent dates)
- ✅ PII removed from ML curated table
- ✅ Proper join logic between datasets
- ✅ Stand-out: Consent timestamp filtering in accelerometer

## 📸 Screenshot Requirements
- Glue Studio job graphs (6 jobs)
- Athena table queries showing counts and sample data
- Error-free job execution logs

Your project is **READY FOR SUBMISSION** after AWS deployment! 🎉