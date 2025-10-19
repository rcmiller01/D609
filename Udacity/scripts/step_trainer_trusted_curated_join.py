
"""step_trainer_trusted_curated_join.py"""
import sys
from pyspark.sql import SparkSession, functions as F

def main(step_trainer_landing: str, customer_curated: str, output_path: str):
    spark = SparkSession.builder.appName("step_trainer_trusted_curated_join").getOrCreate()
    st = spark.read.json(step_trainer_landing)
    cc = spark.read.parquet(customer_curated)
    st = st.withColumn("serialNumber", F.trim(F.col("serialNumber")))
    cc = cc.withColumn("serialNumber", F.trim(F.col("serialNumber")))
    joined = st.alias("s").join(cc.select("serialNumber").dropDuplicates().alias("c"), "serialNumber", "inner")
    result = joined.select([F.col(f"s.{c}") for c in st.columns]).dropDuplicates(["serialNumber","sensorReadingTime"])
    result.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("Usage: spark-submit step_trainer_trusted_curated_join.py <step_trainer_landing> <customer_curated> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
