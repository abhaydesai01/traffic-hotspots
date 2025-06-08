from pyspark.sql import SparkSession
import subprocess

# Step 1: Download latest data from S3 before processing
subprocess.run(["python", "scripts/preload_data.py"], check=True)

spark = SparkSession.builder.appName("TrafficHotspot").getOrCreate()

df = spark.read.csv("collisions.csv", header=True, inferSchema=True)

hotspots = df.filter("LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL") \
    .groupBy("ZIP CODE", "LATITUDE", "LONGITUDE").count() \
    .orderBy("count", ascending=False)

# Convert to Pandas and save as one file
hotspots_df = hotspots.toPandas()
hotspots_df.to_json("output/hotspots.json", orient="records")

spark.stop()
