
"""customer_trusted_to_curated.py"""
import sys
from pyspark.sql import SparkSession, functions as F

def main(customer_trusted: str, accelerometer_trusted: str, output_path: str):
    spark = SparkSession.builder.appName("customer_trusted_to_curated").getOrCreate()
    cust = spark.read.parquet(customer_trusted).withColumn("email", F.lower(F.trim(F.col("email"))))
    acc = spark.read.parquet(accelerometer_trusted).withColumn("user", F.lower(F.trim(F.col("user"))))
    joined = cust.alias("c").join(acc.alias("a"), F.col("c.email")==F.col("a.user"), "inner")
    result = joined.select([F.col(f"c.{c}") for c in cust.columns]).dropDuplicates()
    result.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("Usage: spark-submit customer_trusted_to_curated.py <customer_trusted> <accelerometer_trusted> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
