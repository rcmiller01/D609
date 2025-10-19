
"""customer_landing_to_trusted.py"""
import sys
from pyspark.sql import SparkSession, functions as F
from etl_common import to_epoch_ms, dedupe

def main(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("customer_landing_to_trusted").getOrCreate()
    df = spark.read.json(input_path)
    for c in ["registrationDate","lastUpdateDate","shareWithResearchAsOfDate","shareWithPublicAsOfDate","shareWithFriendsAsOfDate"]:
        if c in df.columns: df = df.withColumn(c, to_epoch_ms(c))
    if "email" in df.columns: df = df.withColumn("email", F.lower(F.trim(F.col("email"))))
    df = df.filter(F.col("shareWithResearchAsOfDate").isNotNull())
    if "email" in df.columns: df = dedupe(df, ("email",))
    (df.withColumn("email_bucket", F.substring(F.col("email"),1,1))
       .write.mode("overwrite").partitionBy("email_bucket").parquet(output_path))
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: spark-submit customer_landing_to_trusted.py <input_path> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
