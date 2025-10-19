
-- Landing
SELECT COUNT(*) FROM stedi_db.customer_landing;
SELECT COUNT(*) FROM stedi_db.accelerometer_landing;
SELECT COUNT(*) FROM stedi_db.step_trainer_landing;
SELECT COUNT(*) FROM stedi_db.customer_landing WHERE shareWithResearchAsOfDate IS NULL OR shareWithResearchAsOfDate=0;

-- Trusted
SELECT COUNT(*) FROM stedi_db.customer_trusted;
SELECT COUNT(*) FROM stedi_db.accelerometer_trusted;
SELECT COUNT(*) FROM stedi_db.step_trainer_trusted;

-- Curated
SELECT COUNT(*) FROM stedi_db.customer_curated;
SELECT COUNT(*) FROM stedi_db.machine_learning_curated;
