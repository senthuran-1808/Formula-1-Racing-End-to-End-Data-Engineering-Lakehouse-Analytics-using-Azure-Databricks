# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest circuits.csv file

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

catalog_name

# COMMAND ----------

source_file = f"{landing_folder_path}/circuits.csv"
table_name = f"{catalog_name}.{bronze_schema}.circuits"

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 1 - read csv file using dataframe reader api

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, DoubleType, StringType

circuits_schema = StructType([
    StructField('circuitId', StringType(), True),
    StructField('url', StringType(), True),
    StructField('circuitName', StringType(), True),
    StructField('lat', DoubleType(), True),
    StructField('long', DoubleType(), True),
    StructField('locality', StringType(), True),
    StructField('country', StringType(), True)
])

# COMMAND ----------

circuits_df = (spark.read
               .format('csv')
               .option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .schema(circuits_schema)
               .load(source_file))

# COMMAND ----------

display(circuits_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------

from pyspark.sql import functions as F

circuits_final_df = add_ingestion_metadata(circuits_df)

display(circuits_final_df)

# COMMAND ----------

(circuits_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
 )

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.circuits;

# COMMAND ----------

display(spark.table('formula1.bronze.circuits'))