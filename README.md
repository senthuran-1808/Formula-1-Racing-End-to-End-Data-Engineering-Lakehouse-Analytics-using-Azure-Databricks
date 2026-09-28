# 🏎️ Formula 1 Racing - End-to-End Data Engineering & Lakehouse Analytics using Azure Databricks
## 📌 Project Overview

![Uploading ChatGPT Image Sep 28, 2026, 10_59_34 PM.png…]()

This project is an end-to-end **Data Engineering and Analytics Lakehouse project** built using **Azure Databricks**.

The project uses Formula 1 racing data collected from the official Formula 1 data source. The extracted data is available in different file formats such as **CSV and JSON**.

The main objective is to ingest, process, transform and analyze the Formula 1 data and finally generate useful business insights through dashboards and conversational AI.

---

## 🔄 Project Flow

```text
Formula 1 Data
      ↓
CSV / JSON Files
      ↓
Data Ingestion
      ↓
Azure Data Lake Storage
      ↓
Azure Databricks
      ↓
Bronze Layer
      ↓
Silver Layer
      ↓
Gold Layer
      ↓
Data Warehouse / SQL
      ↓
Power BI Dashboard
      ↓
Insights & Analytics
      ↓
Databricks Genie
      ↓
Conversational Data Analysis
```

---

## 🌐 1. Formula 1 Data Source

The project starts with Formula 1 racing data.

The data contains information related to:

* Races
* Drivers
* Constructors
* Circuits
* Race results
* Qualifying
* Lap times
* Pit stops
* Driver standings
* Constructor standings

The extracted data is available in different formats, mainly:

```text
CSV
JSON
```

Different datasets may have different structures, so the ingestion process needs to handle multiple file formats.

---

## 📥 2. Data Ingestion

The extracted Formula 1 files are imported into the Azure data platform.

The raw files are first stored in **Azure Data Lake Storage**.

Example:

```text
Formula 1 Source
      ↓
CSV / JSON
      ↓
Azure Data Lake
      ↓
Databricks
```

The purpose of this stage is to preserve the original source data before applying transformations.

---

# 🥉 3. Bronze Layer

The raw Formula 1 data is loaded into the **Bronze layer**.

The Bronze layer contains the ingested source data with minimal transformation.

```text
Raw CSV
Raw JSON
   ↓
Bronze
```

The main purpose of Bronze is to maintain the original data and provide a reliable starting point for further processing.

---

# 🥈 4. Silver Layer

The Bronze data is processed using **Azure Databricks and PySpark**.

In the Silver layer, the data is cleaned and transformed.

Typical operations include:

* Data cleaning
* Data type conversion
* Removing duplicates
* Handling missing values
* Standardizing columns
* Filtering unwanted records
* Joining related datasets

```text
Bronze
   ↓
Cleaning
   ↓
Transformation
   ↓
Silver
```

The Silver layer contains clean and structured Formula 1 data.

---

# 🥇 5. Gold Layer

The cleaned Silver data is further transformed into business-ready datasets.

Multiple Formula 1 datasets are joined together to create meaningful analytical information.

For example:

```text
Drivers
   +
Races
   +
Results
   +
Constructors
   +
Circuits
```

↓

```text
Business-ready Gold Data
```

The Gold layer is designed mainly for analytics, reporting and dashboard creation.

---

# 🏢 6. Data Warehouse / SQL Analytics

The processed Gold data is made available for analytical querying through the Databricks SQL / warehouse layer.

This allows users to query the prepared datasets without working directly with the raw source files.

Example analysis:

* Driver performance
* Constructor performance
* Race results
* Championship standings
* Driver points
* Constructor points
* Race wins
* Circuit performance
* Season trends

---

# 📊 7. Dashboard Creation

The Gold/warehouse data is used to create dashboards for visualization.

The dashboards convert the processed Formula 1 data into useful insights.

Example insights:

```text
Driver Performance
Constructor Performance
Race Winners
Championship Points
Season Performance
Race Trends
Circuit Analysis
```

Instead of looking at thousands of raw records, users can understand the important information through charts, KPIs and visualizations.

---

# 🤖 8. Databricks Genie

The project also uses **Databricks Genie** to provide a conversational way of interacting with the analytical data.

Instead of writing SQL queries manually, users can ask questions using natural language.

Example:

```text
Which driver scored the most points?
```

```text
Which constructor won the most races?
```

```text
Show the performance of a driver across seasons.
```

```text
Which circuit had the most races?
```

Genie converts the user's natural-language question into an analytical query and provides the result from the underlying data.

---

# 💬 Conversational Data Analysis

The overall idea is:

```text
User Question
      ↓
Databricks Genie
      ↓
Understand Question
      ↓
Query Analytical Data
      ↓
Generate Result
      ↓
User Insight
```

This makes the data more accessible to users who may not know SQL.

---

# 🏗️ Medallion Architecture

The complete project follows the **Medallion Architecture**:

```text
                 Formula 1 Data
                       ↓
                CSV / JSON Files
                       ↓
              Azure Data Lake
                       ↓
              ┌───────────────┐
              │    BRONZE     │
              │   Raw Data    │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │    SILVER     │
              │ Cleaned Data  │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │     GOLD      │
              │ Business Data │
              └───────┬───────┘
                      ↓
             Databricks Warehouse
                      ↓
                Power BI
                      ↓
               Visual Insights
                      ↓
              Databricks Genie
                      ↓
             Conversational AI
```

---

# 🛠️ Technologies Used

* Azure Data Lake Storage
* Azure Databricks
* PySpark
* Spark SQL
* Delta Lake
* Medallion Architecture
* Databricks SQL Warehouse
* Power BI
* Databricks Genie

---

# 🎯 Final Outcome

The project transforms raw Formula 1 racing data into valuable analytical information.

```text
Raw F1 Data
     ↓
Data Ingestion
     ↓
Bronze
     ↓
Silver
     ↓
Gold
     ↓
Warehouse
     ↓
Dashboard
     ↓
Insights
     ↓
Genie
     ↓
Conversational Analytics
```

The final solution provides both **visual analytics through dashboards** and **natural-language interaction with the data through Databricks Genie**.

---
