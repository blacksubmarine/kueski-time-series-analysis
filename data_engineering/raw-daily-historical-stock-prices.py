import kagglehub


# Download latest version
path = kagglehub.dataset_download("ehallmar/daily-historical-stock-prices-1970-2018")

print("Path to dataset files:", path)

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# 1. Start SparkSession
spark = SparkSession.builder \
    .appName("Check PySpark") \
    .master("local[*]") \
    .getOrCreate()

# 2. Define sample data and schema
data = [("Alice", 25), ("Bob", 30), ("Charlie", 22)]
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# 3. Create DataFrame
df = spark.createDataFrame(data, schema)

# 4. Show results
df.show()
