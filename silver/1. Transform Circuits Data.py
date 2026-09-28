# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.circuits"
silver_table = f"{catalog_name}.{silver_schema}.circuits"



# COMMAND ----------

circuits_df = spark.read.option('versionAsOf',1).table(bronze_table)

display(circuits_df)


# COMMAND ----------

circuits_df = spark.table(bronze_table)

# COMMAND ----------

circuits_selected_df = circuits_df.select("circuitId", "circuitName", "lat", "long", "locality","country", "ingestion_timestamp", "source_file")

# COMMAND ----------

from pyspark.sql import functions as F

circuits_selected_df = circuits_df.select(
    F.col("circuitId"), 
    F.col("circuitName"), 
    F.col("lat"),
    F.col("long"),
    F.col("locality"),
    F.col("country"),
    F.col("ingestion_timestamp"),
    F.col("source_file")
)

# COMMAND ----------

'''circuits_renamed_df = circuits_selected_df.withColumnRenamed("circuitId", "circuit_id") \
.withColumnRenamed("circuitName", "circuit_name") \
.withColumnRenamed("lat", "latitude") \
.withColumnRenamed("long", "longitude") \
.withColumnRenamed("locality", "city")'''

circuits_renamed_df = circuits_selected_df.withColumnsRenamed({
    "circuitId": "circuit_id", 
    "circuitName": "circuit_name", 
    "lat": "latitude", 
    "long": "longitude"})

# COMMAND ----------

display(circuits_renamed_df)

# COMMAND ----------

circuits_valid_df = circuits_renamed_df.filter(
    "circuit_id IS NOT NULL"
)

#circuits_valid_df = circuits_renamed_df.filter(F.col("circuit_id").isNotNull())

# COMMAND ----------

display(circuits_valid_df)

# COMMAND ----------

cirucits_distinct_df = circuits_valid_df.distinct()
display(cirucits_distinct_df)

cirucits_distinct_df = circuits_valid_df.dropDuplicates(['circuit_id'])


# COMMAND ----------

circuits_final_df = (cirucits_distinct_df
                     .withColumn('circuit_name', F.initcap(F.col("circuit_name")))
                     .withColumn('locality', F.initcap(F.col("locality")))
                     )

# COMMAND ----------

display(circuits_final_df)

# COMMAND ----------

(circuits_final_df
 .write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(silver_table)
 )

# COMMAND ----------

display(spark.read.table(silver_table))