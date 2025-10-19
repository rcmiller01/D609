
"""accelerometer_landing_to_trusted.py"""
import sys
from pyspark.sql import SparkSession, functions as F
from etl_common import to_epoch_ms

def main(acc_input: str, cust_trusted: str, output_path: str):
    spark = SparkSession.builder.appName("accelerometer_landing_to_trusted").getOrCreate()
    acc = spark.read.json(acc_input)
    if "timeStamp" in acc.columns and "timestamp" not in acc.columns:
        acc = acc.withColumnRenamed("timeStamp","timestamp")
    acc = acc.withColumn("timestamp", to_epoch_ms("timestamp")).withColumn("user", F.lower(F.trim(F.col("user"))))
    cust = spark.read.parquet(cust_trusted).withColumn("email", F.lower(F.trim(F.col("email"))))
    joined = acc.alias("a").join(cust.alias("c"), F.col("a.user")==F.col("c.email"), "inner")
    if "shareWithResearchAsOfDate" in joined.columns:
        joined = joined.filter(F.col("a.timestamp") >= F.col("c.shareWithResearchAsOfDate"))
    out_cols = [c for c in acc.columns]
    result = joined.select([F.col(f"a.{c}") for c in out_cols])
    result.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("Usage: spark-submit accelerometer_landing_to_trusted.py <acc_input> <cust_trusted> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
