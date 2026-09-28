# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.races"
silver_table = f"{catalog_name}.{silver_schema}.races"



# COMMAND ----------

races_df = spark.read.option('versionAsOf',1).table(bronze_table)

display(races_df)


# COMMAND ----------

raaces_df = spark.table(bronze_table)

# COMMAND ----------

races_selected_df = races_df.select("season", "round", "raceName","date", "circuitId", "ingestion_timestamp", "source_file")
display(races_selected_df)

# COMMAND ----------

from pyspark.sql import functions as F

races_selected_df = races_df.select(
    F.col("season"), 
    F.col("round"), 
    F.col("raceName"),
    F.col("date"),
    F.col("circuitId"),
    F.col("ingestion_timestamp"),
    F.col("source_file")
)

# COMMAND ----------

'''circuits_renamed_df = circuits_selected_df.withColumnRenamed("circuitId", "circuit_id") \
.withColumnRenamed("circuitName", "circuit_name") \
.withColumnRenamed("lat", "latitude") \
.withColumnRenamed("long", "longitude") \
.withColumnRenamed("locality", "city")'''

races_renamed_df = races_selected_df.withColumnsRenamed({
    "circuitId": "circuit_id", 
    "raceName": "race_name", 
    "date": "race_date"})

# COMMAND ----------

display(races_renamed_df)

# COMMAND ----------

'''races_valid_df = races_renamed_df.filter(
    "circuit_id IS NOT NULL"
)'''

races_valid_df = races_renamed_df.filter(F.col("circuit_id").isNotNull())

# COMMAND ----------

display(races_valid_df)

# COMMAND ----------

races_distinct_df = races_valid_df.distinct()
display(races_distinct_df)

races_distinct_df = races_valid_df.dropDuplicates(['season','round'])


# COMMAND ----------

races_final_df = (races_distinct_df
                     .withColumn('race_name', F.initcap(F.col("race_name")))
                    # .withColumn('locality', F.initcap(F.col("locality")))
                     )

# COMMAND ----------

display(races_final_df)

# COMMAND ----------

(races_final_df
 .write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(silver_table)
 )

# COMMAND ----------

display(spark.read.table(silver_table))