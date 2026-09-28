# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest drivers.csv file

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

source_file = f"{landing_folder_path}/drivers.json"
table_name = f"{catalog_name}.{bronze_schema}.drivers"

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 1 - read json file using dataframe reader api

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DateType


name_schema = StructType([
    StructField('givenName', StringType(), True),
    StructField('familyName', StringType(), True)
])

drivers_schema = StructType(fields=[
  StructField('driverId', StringType(), True),
  StructField('name', name_schema),
  StructField('dateOfBirth', DateType(), True),
  StructField('nationality', StringType(), True),
  StructField('url', StringType(), True)
])



'''
cons_schema = """constructorID STRING,
                 name STRING,
                nationality STRING,
                url STRING"""


'''

# COMMAND ----------

drivers_df = (spark.read
               .format('json')
               .option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .schema(drivers_schema)
               .load(source_file))

# COMMAND ----------

display(drivers_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------


drivers_final_df = add_ingestion_metadata(drivers_df)

display(drivers_final_df)


# COMMAND ----------

(drivers_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
)

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.drivers;

# COMMAND ----------

display(spark.table(table_name))

# COMMAND ----------

# MAGIC %md
# MAGIC