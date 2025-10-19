
"""machine_learning_curated.py"""
import sys
from pyspark.sql import SparkSession, functions as F

def main(step_trainer_trusted: str, accelerometer_trusted: str, customer_curated: str, output_path: str):
    spark = SparkSession.builder.appName("machine_learning_curated").getOrCreate()
    st = spark.read.parquet(step_trainer_trusted)
    acc = spark.read.parquet(accelerometer_trusted)
    cc = spark.read.parquet(customer_curated)
    if "timeStamp" in acc.columns and "timestamp" not in acc.columns:
        acc = acc.withColumnRenamed("timeStamp","timestamp")
    st = st.withColumnRenamed("sensorReadingTime","timestamp").withColumn("timestamp", F.col("timestamp").cast("bigint"))
    acc = acc.withColumn("user", F.lower(F.trim(F.col("user"))))
    cc = cc.withColumn("email", F.lower(F.trim(F.col("email")))).withColumn("serialNumber", F.trim(F.col("serialNumber")))
    st = st.withColumn("serialNumber", F.trim(F.col("serialNumber")))
    acc_cc = acc.alias("a").join(cc.alias("c"), F.col("a.user")==F.col("c.email"), "inner")
    joined = acc_cc.alias("ac").join(
        st.alias("s"),
        (F.col("ac.c.serialNumber")==F.col("s.serialNumber")) & (F.col("ac.a.timestamp")==F.col("s.timestamp")),
        "inner"
    )
    out = joined.select(
        F.col("ac.a.timestamp").alias("timestamp"),
        F.col("ac.a.x"), F.col("ac.a.y"), F.col("ac.a.z"),
        F.col("s.distanceFromObject"),
        F.col("ac.c.serialNumber").alias("serialNumber")
    )
    out.write.mode("overwrite").parquet(output_path)
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("Usage: spark-submit machine_learning_curated.py <step_trainer_trusted> <accelerometer_trusted> <customer_curated> <output_path>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
