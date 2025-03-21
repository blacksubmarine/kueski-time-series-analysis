import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, to_date
from pyspark.sql.window import Window

os.environ["PYSPARK_PYTHON"] = r".venv\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r".venv\Scripts\python.exe"


# Initialize SparkSession
spark = (
    SparkSession.builder.appName("Stock Prices with Company Info")
    .master("local[*]")
    # Disable Hadoop native IO
    .config("spark.hadoop.hadoop.native.lib", "false")
    .config("spark.hadoop.io.native.lib.available", "false")
    # Force file system to be pure Java RawLocal
    .config("spark.hadoop.fs.file.impl.disable.cache", "true")
    .getOrCreate()
)

# Build base path dynamically from current Windows username
user = os.getenv("USERNAME")
base_path = rf"C:\Users\{user}\.cache\kagglehub\datasets\ehallmar\daily-historical-stock-prices-1970-2018\versions\1"
prices_path = f"{base_path}\\historical_stock_prices.csv"
stocks_path = f"{base_path}\\historical_stocks.csv"

# Load price data
df_prices = (
    spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(prices_path)
    .withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
)

# Load stock metadata
df_stocks = (
    spark.read.option("header", True).option("inferSchema", True).csv(stocks_path)
)

# Show previews
df_prices.show(3)
df_stocks.show(3)

# Select two tickers for analysis
selected_tickers = ["AHH", "PIH"]

# Filter and sort by date
filtered = df_prices.filter(col("ticker").isin(selected_tickers)).orderBy(
    "ticker", "date"
)

# Define 7-day rolling window
rolling_window = Window.partitionBy("ticker").orderBy("date").rowsBetween(-6, 0)

# Add moving average column
df_result = filtered.withColumn("moving_avg_7d", avg("close").over(rolling_window))

# Show results
df_result.select("ticker", "date", "close", "moving_avg_7d").show(15)

# Clean shutdown

# Get current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "stock_moving_avg.parquet")

# # Write result as Parquet
# (
#     df_result.coalesce(1)
#     .write
#     .option("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
#     .mode("overwrite")
#     .parquet(output_path)
# )

if os.path.exists(output_path):
    os.remove(output_path)

df_result.toPandas().to_parquet(output_path, index=False)

# Stop Spark
spark.stop()
