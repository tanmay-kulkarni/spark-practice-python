"""
Simple Spark EDA Example
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, desc

# Initialize Spark
spark = SparkSession.builder.appName("Simple EDA").getOrCreate()
print(f"Spark Version: {spark.version}")

# Create a simple dataset
data = [
    ("Laptop", "Electronics", 1200, 5),
    ("Phone", "Electronics", 800, 10),
    ("Headphones", "Audio", 100, 20),
    ("TV", "Electronics", 1500, 3),
    ("Speaker", "Audio", 200, 15),
    ("Tablet", "Electronics", 600, 8),
    ("Camera", "Electronics", 700, 4),
    ("Smartwatch", "Wearables", 300, 12)
]

# Create DataFrame
df = spark.createDataFrame(data, ["product", "category", "price", "stock"])

# Display sample
print("\n--- Sample Data ---")
df.show()

# Basic stats
print("\n--- Basic Statistics ---")
df.describe().show()

# Category summary
print("\n--- Category Analysis ---")
category_summary = df.groupBy("category") \
    .agg(
        count("*").alias("product_count"),
        sum("stock").alias("total_stock"),
        avg("price").alias("avg_price")
    ) \
    .orderBy("category")

category_summary.show()

# Save category summary
print("\nSaving category summary...")
category_summary.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/output/category_summary")

# Product analysis
print("\n--- Product Analysis ---")
product_analysis = df.select(
    "product", 
    "category", 
    "price", 
    "stock", 
    (col("price") * col("stock")).alias("inventory_value")
).orderBy(desc("inventory_value"))

product_analysis.show()

# Save product analysis
print("\nSaving product analysis...")
product_analysis.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("/output/product_analysis")

print("\nEDA completed. Results saved to output directory.")
spark.stop()