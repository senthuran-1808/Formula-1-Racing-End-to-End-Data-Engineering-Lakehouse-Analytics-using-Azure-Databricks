# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest races.csv file

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

source_file = f"{landing_folder_path}/races.csv"
table_name = f"{catalog_name}.{bronze_schema}.races"

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 1 - read csv file using dataframe reader api

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

races_schema = StructType([
    StructField('season', IntegerType(), True),
    StructField('round', IntegerType(), True),
    StructField('url', StringType(), True),
    StructField('raceName', StringType(), True),
    StructField('date', DateType(), True),
    StructField('circuitId', StringType(), True),
])

# COMMAND ----------

races_df = (spark.read
               .format('csv')
               .option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .schema(races_schema)
               .load(source_file))

# COMMAND ----------

display(races_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------



races_final_df = add_ingestion_metadata(races_df)

display(races_final_df)

# COMMAND ----------

(races_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
)

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.races;

# COMMAND ----------

display(spark.table(table_name))