# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.results"
silver_table = f"{catalog_name}.{silver_schema}.results"



# COMMAND ----------

results_df = spark.read.table(bronze_table)

display(results_df)


# COMMAND ----------

results_df = spark.table(bronze_table)

# COMMAND ----------

results_dropped_df = results_df.drop("url")


# COMMAND ----------

'''from pyspark.sql import functions as F

cons_selected_df = cons_df.select(
    F.col("constructorId"), 
    F.col("name"), 
    F.col("nationality"),
    F.col("ingestion_timestamp"),
    F.col("source_file")
)'''

# COMMAND ----------

#cons_renamed_df = cons_df.drop("url")

# COMMAND ----------

'''circuits_renamed_df = circuits_selected_df.withColumnRenamed("circuitId", "circuit_id") \
.withColumnRenamed("circuitName", "circuit_name") \
.withColumnRenamed("lat", "latitude") \
.withColumnRenamed("long", "longitude") \
.withColumnRenamed("locality", "city")'''

results_renamed_df = results_dropped_df.withColumnsRenamed({
    "driverId": "driver_id", 
    "constructorID": "constructor_id", 
    "raceName":"race_name",
    "date":"race_date",
    "grid":"grid_position",
    "laps":"completed_laps",
    "number":"car_number",
    "position":"final_position",
    "positionText":"grid_position_text"
    })

# COMMAND ----------

display(results_renamed_df)

# COMMAND ----------

'''races_valid_df = races_renamed_df.filter(
    "circuit_id IS NOT NULL"
)'''

from pyspark.sql import functions as F

results_valid_df = (results_renamed_df
                    .filter(
                        F.col("season").isNotNull() &
                        F.col("round").isNotNull() &
                        F.col("constructor_id").isNotNull() & 
                        F.col("driver_id").isNotNull())
                    
                    )

# COMMAND ----------

display(results_dropped_df.count() - results_valid_df.count())

# COMMAND ----------

#drivers_distinct_df = drivers_valid_df.distinct()
#display(drivers_distinct_df)

results_distinct_df = results_valid_df.dropDuplicates(['season','round','driver_id'])

display(results_valid_df.count() - results_distinct_df.count())


# COMMAND ----------

results_final_df = (results_distinct_df
                     .withColumn('race_name', F.initcap(F.col("race_name" )))
                    # .withColumn('locality', F.initcap(F.col("locality")))
                     )

# COMMAND ----------

display(results_final_df)

# COMMAND ----------

(results_final_df
 .write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(silver_table)
 )

# COMMAND ----------

display(spark.read.table(silver_table))