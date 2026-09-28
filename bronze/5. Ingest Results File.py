# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest results folder

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

source_file = f"{landing_folder_path}/results"
table_name = f"{catalog_name}.{bronze_schema}.results"

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 1 - read json file using dataframe reader api

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, FloatType
'''
cons_schema = """constructorID STRING,
                 name STRING,
                nationality STRING,
                url STRING"""


'''
results_schema = StructType(fields=[
  StructField('constructorId', StringType(), True),
  StructField('date', DateType(), True),
  StructField('raceName', StringType(), True),
  StructField('round', IntegerType(), True),
  StructField('season', IntegerType(),True),
  StructField('url', StringType(), True),
  StructField('driverId', StringType(), True),
  StructField('grid', IntegerType(), True),
  StructField('laps', IntegerType(), True),
  StructField('number', IntegerType(), True),
  StructField('points', FloatType(), True),
  StructField('position', IntegerType(), True),
  StructField('positionText', StringType(), True),
  StructField('status', StringType(),)

])

# COMMAND ----------

results_df = (spark.read
               .format('json')
               #.option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .schema(results_schema)
               .load(source_file))

# COMMAND ----------

display(results_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------


results_final_df = add_ingestion_metadata(results_df)

display(results_final_df)


# COMMAND ----------

(results_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
)

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.results;

# COMMAND ----------

display(spark.table(table_name))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT season, count(*) FROM formula1.bronze.results GROUP BY season ORDER BY season DESC