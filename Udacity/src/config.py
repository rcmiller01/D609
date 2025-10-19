
"""Configuration defaults for local dev and AWS runs."""
from dataclasses import dataclass

@dataclass
class Paths:
    customer_landing: str = "s3://your-bucket/landing/customer/"
    accelerometer_landing: str = "s3://your-bucket/landing/accelerometer/"
    step_trainer_landing: str = "s3://your-bucket/landing/step_trainer/"
    customer_trusted: str = "s3://your-bucket/trusted/customer/"
    accelerometer_trusted: str = "s3://your-bucket/trusted/accelerometer/"
    step_trainer_trusted: str = "s3://your-bucket/trusted/step_trainer/"
    customer_curated: str = "s3://your-bucket/curated/customer/"
    machine_learning_curated: str = "s3://your-bucket/curated/ml_ready/"
GLUE_DATABASE = "stedi_db"
