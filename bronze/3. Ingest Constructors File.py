# Databricks notebook source
# MAGIC %md
# MAGIC ##Ingest constructors.csv file

# COMMAND ----------

# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

# MAGIC %run "../common/2.bronze-helpers"

# COMMAND ----------

source_file = f"{landing_folder_path}/constructors.json"
table_name = f"{catalog_name}.{bronze_schema}.constructors"

# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 1 - read json file using dataframe reader api

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
'''
cons_schema = """constructorID STRING,
                 name STRING,
                nationality STRING,
                url STRING"""


'''
cons_schema = StructType(fields=[
  StructField('constructorId', StringType(), True),
  StructField('name', StringType(), True),
  StructField('nationality', StringType(), True),
  StructField('url', StringType(), True)

])

# COMMAND ----------

constructors_df = (spark.read
               .format('json')
               .option('header', True)
               #.option('inferSchema', True)
               .option('mode','FAILFAST')
               .schema(cons_schema)
               .load(source_file))

# COMMAND ----------

display(constructors_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Step 2 - metadata columns

# COMMAND ----------


constructors_final_df = add_ingestion_metadata(constructors_df)

display(constructors_final_df)


# COMMAND ----------

(constructors_final_df
 .write
 .mode('overwrite')
 .format('delta')
 .saveAsTable(table_name)
)

#display(dbutils.fs.ls('/Volumes/formula1/processed/circuits')

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * FROM formula1.bronze.constructors;

# COMMAND ----------

display(spark.table(table_name))