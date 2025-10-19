
# Udacity STEDI Project — Rubric Checklist
[...trimmed for brevity in this header — full list below...]

## Landing Zone
- [ ] Glue Studio ingestion from S3 (3 jobs)
- [ ] Manual Glue Tables with typed JSON (3 tables)
- [ ] Athena counts: 956 / 81273 / 28680; plus blank-consent count

## Trusted Zone
- [ ] Schema update enabled
- [ ] customer_trusted count: 482 (no blank consent)
- [ ] accelerometer_trusted count: 40981 (or 32025 stand-out)
- [ ] step_trainer_trusted count: 14460

## Curated Zone
- [ ] customer_curated: 482 (or 464 stand-out)
- [ ] machine_learning_curated: 43681 (or 34437)
- [ ] Final ML table drops PII (email/name/phone)

### Full Version
(Keep this section in your copy)
- Glue Studio ingestion nodes for each landing dataset are present.
- DDLs include all JSON fields and real types.
- Athena screenshots show counts & sample rows.
- customer_trusted filters out blank consent.
- accelerometer_trusted is inner-joined to customer_trusted by email and keeps only accelerometer columns.
- customer_curated keeps only customer columns; step_trainer is filtered by serialNumber ∈ customer_curated.
- machine_learning_curated joins by timestamp & device; final table anonymized.
