# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.drivers"
silver_table = f"{catalog_name}.{silver_schema}.drivers"



# COMMAND ----------

drivers_df = spark.read.table(bronze_table)

display(drivers_df)


# COMMAND ----------

drivers_df = spark.table(bronze_table)

# COMMAND ----------

drivers_dropped_df = drivers_df.drop("url")


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

drivers_renamed_df = drivers_dropped_df.withColumnsRenamed({
    "driverId": "driver_id", 
    "dateOfBirth": "date_of_birth", 
    })

# COMMAND ----------

display(drivers_renamed_df)

# COMMAND ----------

from pyspark.sql import functions as F
drivers_concatenated_df = (
    drivers_renamed_df
    .withColumn("driver_name",
                F.initcap(F.concat_ws(" ",F.col("name.givenName"), F.col("name.familyName")))).drop("name")
)

# COMMAND ----------

display(drivers_concatenated_df)

# COMMAND ----------

'''races_valid_df = races_renamed_df.filter(
    "circuit_id IS NOT NULL"
)'''

drivers_valid_df = drivers_concatenated_df.filter(F.col("driver_id").isNotNull())

# COMMAND ----------

display(drivers_valid_df)

# COMMAND ----------

drivers_distinct_df = drivers_valid_df.distinct()
display(drivers_distinct_df)

drivers_distinct_df = drivers_valid_df.dropDuplicates(['driver_id'])


# COMMAND ----------

drivers_final_df = (drivers_distinct_df
                     .withColumn('nationality', F.initcap(F.col("nationality" )))
                    # .withColumn('locality', F.initcap(F.col("locality")))
                     )

# COMMAND ----------

display(drivers_final_df)

# COMMAND ----------

(drivers_final_df
 .write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(silver_table)
 )

# COMMAND ----------

display(spark.read.table(silver_table))