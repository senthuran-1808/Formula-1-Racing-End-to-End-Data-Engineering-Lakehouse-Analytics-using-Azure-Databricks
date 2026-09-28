# Databricks notebook source
# MAGIC %run "../common/1. environmnet-config"

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.constructors"
silver_table = f"{catalog_name}.{silver_schema}.constructors"



# COMMAND ----------

cons_df = spark.read.option('versionAsOf',0).table(bronze_table)

display(cons_df)


# COMMAND ----------

cons_df = spark.table(bronze_table)

# COMMAND ----------

cons_selected_df = cons_df.select("constructorId", "name", "nationality", "ingestion_timestamp", "source_file")
display(cons_selected_df)

# COMMAND ----------

from pyspark.sql import functions as F

cons_selected_df = cons_df.select(
    F.col("constructorId"), 
    F.col("name"), 
    F.col("nationality"),
    F.col("ingestion_timestamp"),
    F.col("source_file")
)

# COMMAND ----------

cons_renamed_df = cons_df.drop("url")

# COMMAND ----------

'''circuits_renamed_df = circuits_selected_df.withColumnRenamed("circuitId", "circuit_id") \
.withColumnRenamed("circuitName", "circuit_name") \
.withColumnRenamed("lat", "latitude") \
.withColumnRenamed("long", "longitude") \
.withColumnRenamed("locality", "city")'''

cons_renamed_df = cons_selected_df.withColumnsRenamed({
    "constructorId": "constructor_id", 
    "name": "constructor_name", 
    })

# COMMAND ----------

display(cons_renamed_df)

# COMMAND ----------

'''races_valid_df = races_renamed_df.filter(
    "circuit_id IS NOT NULL"
)'''

cons_valid_df = cons_renamed_df.filter(F.col("constructor_id").isNotNull())

# COMMAND ----------

display(cons_valid_df)

# COMMAND ----------

cons_distinct_df = cons_valid_df.distinct()
display(cons_distinct_df)

cons_distinct_df = cons_valid_df.dropDuplicates()


# COMMAND ----------

cons_final_df = (cons_distinct_df
                     .withColumn('nationality', F.initcap(F.col("nationality" )))
                    # .withColumn('locality', F.initcap(F.col("locality")))
                     )

# COMMAND ----------

display(cons_final_df)

# COMMAND ----------

(cons_final_df
 .write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(silver_table)
 )

# COMMAND ----------

display(spark.read.table(silver_table))