# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

target_table = f"{catalog_name}.{gold_schema}.fact_results"

# COMMAND ----------

target_table

# COMMAND ----------

results_df = (
    spark.table(f"{catalog_name}.{silver_schema}.results")
    .withColumn("session_type", F.lit("RACE"))
    .drop("race_name", "race_date","ingestion_timestamp","source_file")
)
#ref_nationality_df = spark.table(f"{catalog_name}.{gold_schema}.ref_nationality_region")

# COMMAND ----------

sprints_df = (
    spark.table(f"{catalog_name}.{silver_schema}.sprints")
    .withColumn("session_type", F.lit("SPRINT"))
    .drop("race_name", "race_date","ingestion_timestamp","source_file")
)

# COMMAND ----------

results_sprints_df = results_df.unionByName(sprints_df)
display(results_sprints_df)


# COMMAND ----------

fact_session_results_df = (
    results_sprints_df
    .withColumn("is_win", F.col("final_position") == 1)
    .withColumn("is_podium", F.col("final_position").between(1,3))
    .withColumn("has_points", F.col("points")>0)


)

# COMMAND ----------

display(fact_session_results_df)

# COMMAND ----------

(
   fact_session_results_df
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(target_table)
)

# COMMAND ----------

display(spark.table(target_table))