
"""Common ETL utilities for Glue-style PySpark jobs."""
from typing import Tuple
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T

def to_epoch_ms(col):
    return (
        F.when(F.col(col).cast("double").isNotNull(),
               F.when(F.col(col) > 1_000_000_000_000, F.col(col).cast("bigint"))
                .otherwise((F.col(col).cast("double")*1000).cast("bigint"))
        )
        .otherwise(F.to_timestamp(F.col(col)).cast("bigint")*1000)
    )

def dedupe(df: DataFrame, keys: Tuple[str, ...]) -> DataFrame:
    from pyspark.sql.window import Window
    ts = None
    for c in ["lastUpdateDate","registrationDate","timeStamp","sensorReadingTime"]:
        if c in df.columns:
            ts = c
            break
    w = Window.partitionBy(*keys).orderBy(F.desc(ts)) if ts else Window.partitionBy(*keys).orderBy(F.desc(F.monotonically_increasing_id()))
    return (df.withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn")==1).drop("_rn"))

def anonymize_customer_columns(df: DataFrame) -> DataFrame:
    """Remove PII columns for ML curated table - required by rubric"""
    drop_cols = [c for c in ["email","phone","customerName"] if c in df.columns]
    return df.drop(*drop_cols)
