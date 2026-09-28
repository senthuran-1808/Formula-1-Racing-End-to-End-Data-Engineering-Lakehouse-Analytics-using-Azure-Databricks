# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW formula1.gold.v_driver_standing
# MAGIC AS
# MAGIC WITH driver_session_summary
# MAGIC AS
# MAGIC (
# MAGIC SELECT r.season,
# MAGIC        d.driver_id,
# MAGIC        d.driver_name,
# MAGIC        d.nationality,
# MAGIC        COUNT(*) AS race_starts,
# MAGIC        SUM(r.points) AS total_points,
# MAGIC        COUNT_IF(r.is_win = true) AS number_of_wins,
# MAGIC        COUNT_IF(r.is_podium = true) AS number_of_podiums 
# MAGIC        FROM formula1.gold.fact_results r
# MAGIC        JOIN formula1.gold.dim_drivers d
# MAGIC        ON r.driver_id = d.driver_id
# MAGIC        GROUP BY r.season,
# MAGIC             d.driver_id,
# MAGIC             d.driver_name,
# MAGIC             d.nationality
# MAGIC )
# MAGIC
# MAGIC SELECT season, driver_id, driver_name, nationality, 
# MAGIC        RANK() OVER(PARTITION BY season ORDER BY total_points DESC, number_of_wins DESC) AS standing,
# MAGIC        race_starts, total_points, number_of_wins, number_of_podiums
# MAGIC        FROM driver_session_summary;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM formula1.gold.v_driver_standing
# MAGIC WHERE season = 2025;