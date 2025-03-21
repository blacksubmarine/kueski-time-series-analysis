# PySpark Setup on Windows 11 (with Virtual Environment)

This guide explains how to set up PySpark, Hadoop, and winutils.exe on Windows 11 using a virtual environment and optional Jupyter/VSCode integration.

## 1. Create and Activate Virtual Environment

    python -m venv .venv
    .venv\Scripts\activate

## 2. Install Python Dependencies

    pip install pyspark pandas kagglehub ipywidgets notebook

## 3. requirements.txt

    pyspark
    pandas
    kagglehub
    ipywidgets
    notebook

## 4. Set PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON (Permanent)

Use Command Prompt to set these environment variables:

    setx PYSPARK_PYTHON "C:\Users\52562\Documents\GitHub\kueski-time-series-analysis\.venv\Scripts\python.exe"
    setx PYSPARK_DRIVER_PYTHON "C:\Users\52562\Documents\GitHub\kueski-time-series-analysis\.venv\Scripts\python.exe"

Alternatively, set them via: System Properties > Environment Variables.

## 5. Optional: Set Variables Inside Jupyter or Interactive Window

If running code in Jupyter or the VSCode Interactive window, use:

    import os
    os.environ["PYSPARK_PYTHON"] = r"C:\Users\52562\Documents\GitHub\kueski-time-series-analysis\.venv\Scripts\python.exe"
    os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\52562\Documents\GitHub\kueski-time-series-analysis\.venv\Scripts\python.exe"

## 6. Fix tqdm / IProgress Warnings

    pip install ipywidgets notebook
    jupyter nbextension enable --py widgetsnbextension --sys-prefix
    jupyter nbextension install --py widgetsnbextension --sys-prefix

## 7. Set Up Hadoop and winutils.exe

Download `winutils.exe`:

1. Go to: https://github.com/cdarlint/winutils/tree/master/hadoop-3.3.1/bin
2. Download `winutils.exe`
3. Place it in: `C:\hadoop\bin`

Then set the environment variables:

    setx HADOOP_HOME "C:\hadoop"
    setx PATH "%PATH%;C:\hadoop\bin"

## 8. Test Spark Setup

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder
        .appName("Test PySpark")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.createDataFrame([("Alice", 25), ("Bob", 30)], ["name", "age"])
    df.show()

## 9. Verify Python Path Used by Spark

    import sys
    print(sys.executable)

Expected output:

    C:\Users\52562\Documents\GitHub\kueski-time-series-analysis\.venv\Scripts\python.exe

## 10. Additional Notes

- Activate venv in PowerShell: `.\.venv\Scripts\Activate`
- Activate venv in CMD: `.venv\Scriptsctivate`
- Deactivate venv: `deactivate`

## 11. Troubleshooting

- If you see "python3 not found", set `PYSPARK_PYTHON` and `PYSPARK_DRIVER_PYTHON`
- If Spark complains about missing winutils.exe, ensure `winutils.exe` exists in `C:\hadoop\bin` and `HADOOP_HOME` is set
