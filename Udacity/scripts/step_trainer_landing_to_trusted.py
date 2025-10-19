
"""step_trainer_landing_to_trusted.py"""
import sys
from pyspark.sql import SparkSession, functions as F
from etl_common import to_epoch_ms

def main(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("step_trainer_landing_to_trusted").getOrCreate()
    df = spark.read.json(input_path)
    if "sensorReadingTime" in df.columns: df = df.withColumn("sensorReadingTime", to_epoch_ms("sensorReadingTime"))
    if "distanceFromObject" in df.columns: df = df.withColumn("distanceFromObject", F.col("distanceFromObject").cast("int"))
    if all(c in df.columns for c in ["serialNumber","sensorReadingTime"]):
        df = df.dropDuplicates(["serialNumber","sensorReadingTime"])
    df.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: spark-submit step_trainer_landing_to_trusted.py <input_path> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
