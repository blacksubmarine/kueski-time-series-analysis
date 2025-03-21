# PySpark Setup on Windows 11 (with Virtual Environment)

This guide summarizes the required setup for running PySpark with Hadoop on Windows

## 1. Activate the Virtual Environment

In PowerShell or CMD:

    .venv\Scripts\activate

## 2. Install Python Dependencies

    pip install -r requirements.txt

Ensure the `requirements.txt` file includes:

    pyspark
    pandas
    kagglehub
    ipywidgets
    notebook

## 3. Set Up Hadoop and winutils.exe

1. Download `winutils.exe` from:
   https://github.com/cdarlint/winutils/tree/master/hadoop-3.3.1/bin

2. Place it in:

    C:\hadoop\bin\winutils.exe

3. Make sure the following environment variables are set. These are already defined in the `.env` file:

    HADOOP_HOME=C:\hadoop
    PYSPARK_PYTHON=.venv\Scripts\python.exe
    PYSPARK_DRIVER_PYTHON=.venv\Scripts\python.exe

Load them into your session using:

    dotenv.load_dotenv(".env")

Or ensure your terminal session has these values applied.

## 4. Fix Interactive Window Issues

If using Jupyter notebooks or the VSCode interactive window:

- Add this to the top of your notebook/script to ensure Spark uses the right Python:

    import os
    os.environ["PYSPARK_PYTHON"] = r".venv\Scripts\python.exe"
    os.environ["PYSPARK_DRIVER_PYTHON"] = r".venv\Scripts\python.exe"

- Fix tqdm/IProgress warnings by running:

    pip install ipywidgets notebook
    jupyter nbextension enable --py widgetsnbextension --sys-prefix
    jupyter nbextension install --py widgetsnbextension --sys-prefix

## 5. Run PySpark

Example test:

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder
        .appName("Test")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.createDataFrame([("Alice", 25)], ["name", "age"])
    df.show()
