# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1.bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1.silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1.gold;
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1.landing;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS formula1.landing.raw
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog();

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG formula1;