from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, desc, expr, round, min as min_func, max as max_func
import random
import os
from datetime import datetime

# Create Spark session
spark = SparkSession.builder \
    .appName("Spark Demo") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Create more interesting sample data
num_records = 10000
products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones"]
categories = ["Electronics", "Accessories", "Gaming", "Office"]
locations = ["North", "South", "East", "West", "Central"]

data = [(i, 
         f"user_{random.randint(1, 100)}", 
         random.choice(products),
         random.choice(categories),
         random.choice(locations), 
         random.randint(10, 1000))
        for i in range(num_records)]

# Create DataFrame
df = spark.createDataFrame(data, ["id", "user", "product", "category", "location", "price"])

print("\nSample Data:")
df.show(5)

# Save basic dataset
output_base = "/output"
raw_output = f"{output_base}/raw_data"
print(f"\nSaving raw data sample to: {raw_output}")
df.limit(100).coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(raw_output)

# Product statistics
product_stats = df.groupBy("product") \
    .agg(count("*").alias("count"), 
         sum("price").alias("total_revenue"), 
         round(avg("price"), 2).alias("avg_price")) \
    .orderBy(desc("count"))

print("\nProduct Statistics:")
product_stats.show()

# Save product statistics
product_output = f"{output_base}/product_stats"
print(f"Saving product statistics to: {product_output}")
product_stats.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(product_output)

# Category analysis
category_stats = df.groupBy("category") \
    .agg(count("*").alias("count"), 
         sum("price").alias("total_revenue"), 
         round(avg("price"), 2).alias("avg_price")) \
    .orderBy(desc("total_revenue"))

print("\nCategory Analysis:")
category_stats.show()

# Save category statistics
category_output = f"{output_base}/category_stats" 
print(f"Saving category analysis to: {category_output}")
category_stats.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(category_output)

# Location analysis with price ranges
location_stats = df.groupBy("location") \
    .agg(count("*").alias("count"),
         round(avg("price"), 2).alias("avg_price"),
         expr("percentile_approx(price, 0.5)").alias("median_price"),
         min_func("price").alias("min_price"),
         max_func("price").alias("max_price"))

print("\nLocation Analysis:")
location_stats.show()

# Save location statistics
location_output = f"{output_base}/location_stats"
print(f"Saving location analysis to: {location_output}")
location_stats.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(location_output)

print("\nDone! Spark job completed successfully.")
print(f"All results saved to the 'output' directory")

spark.stop()