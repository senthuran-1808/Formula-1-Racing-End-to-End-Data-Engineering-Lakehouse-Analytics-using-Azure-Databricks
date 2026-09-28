# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest sprintss folder

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

source_file = f"{landing_folder_path}/sprints"
table_name = f"{catalog_name}.{bronze_schema}.sprints"

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
sprints_schema = StructType(fields=[
  StructField('date', DateType(), True),
  StructField('raceName', StringType(), True),
  StructField('round', IntegerType(), True),
  StructField('season', IntegerType(),True),
  StructField('url', StringType(), True),
  StructField('constructorId', StringType(), True),
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

sprints_df = (spark.read
               .format('json')
               #.option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .option('mutliLine', True)
               .schema(sprints_schema)
               .load(source_file))

# COMMAND ----------

display(sprints_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------


sprints_final_df = add_ingestion_metadata(sprints_df)

display(sprints_final_df)


# COMMAND ----------

(sprints_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
)

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.sprints;

# COMMAND ----------

display(spark.table(table_name))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT season, count(*) 
# MAGIC FROM formula1.bronze.sprints
# MAGIC GROUP BY season 
# MAGIC ORDER BY season DESC