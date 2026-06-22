# 🚀 Celebal Technologies — Data Engineering Internship

![Intern](https://img.shields.io/badge/Role-Data%20Engineering%20Intern-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Tools](https://img.shields.io/badge/Tools-Python%20%7C%20MySQL%20%7C%20SQL-orange)

> A repository documenting my weekly assignments, projects, and learnings  
> during my **Data Engineering Internship at Celebal Technologies**.  
> Each week covers a new concept — from data cleaning to advanced SQL analytics.

---

## 👩‍💻 About Me

**Nidhi Bansal**  
Data Engineering Intern — Celebal Technologies  
📍 Jaipur, Rajasthan, India  
🛠️ Python | SQL | MySQL | Pandas | Jupyter Notebook| ADF

---

## 📁 Repository Structure

```
CEI_DE_WORK/
│
├── Week-01/
│   ├── CELEBAL_WEEK-1.ipynb        # Jupyter notebook 
│   ├── Combined_dataset.csv        # Original raw dataset
│   ├── Combined_dataset_CLEANED.csv # Cleaned output
│   └── readme.md
│
├── Week-02-SQL-Sales-Analysis/
│   ├── CELEBAL_WEEK-2.sql          # Full SQL script 
│   ├── Q23.png                     # Query result screenshot
│   ├── Q5.png                      # Query result screenshot
│   ├── Q6.png                      # Query result screenshot
│   └── readme.md
│
├── Week-03-Advance-SQL-Superstore/
│   ├── CELEBAL_WEEK-3.sql          # Advanced SQL — CTEs, Subqueries, Window Functions
│   └── readme.md
├── WEEK-4-azure-adf-pipeline/
│   ├── screenshot/
│   │   ├── 1-Resource Group.png
│   │   ├── 2-Storage Setup.png
│   │   ├── 2- csv uploaded.png
│   │   ├── 3- linked.png
│   │   ├── 3-source.png
│   │   ├── 3-destination.png
│   │   ├── 3-metadata.png
│   │   ├── 4-pipeline design.png
│   │   ├── 5-pipeline execution.png
│   │   ├── 6-Roles.png
│   │   └── output.png
└── Datasets/
|   └── Sample - Superstore.csv
│   └── Readme.md
│Week-5 Spark-assignment/
├── data/
│   └── dataset.csv        
├── notebook/
│   └── spark_basics.ipynb   
├── output/
│   └── results.csv          
└── README.md                
└── README.md
```                
---

## 📅 Weekly Progress

| Week | Topic | Concepts Covered | Tools |  |
|---|---|---|---|---|
| Week 01 | Python Data Cleaning | Pandas, Missing Values, Data Types, EDA | Python, Jupyter |  |
| Week 02 | SQL Sales Analysis | SELECT, JOINs, Aggregation, Transactions, ACID | MySQL Workbench |  |
| Week 03 | Advanced SQL — Superstore | Subqueries, CTEs, Window Functions, RANK | MySQL Workbench |  |
| Week 04 | Azure Cloud & ADF Pipeline | Blob Storage, ADF, Linked Services, IAM, ETL Pipeline| Microsoft Azure |  |
| Week 05 | Spark-assignment | Apache Spark — DataFrame cleaning, transformation & aggregation| Python, Jupyter  |  |


---

## 🔑 Key Highlights

### 📌 Week 01 — Pandas Data Cleaning
- Cleaned a **1000-row Indian E-Commerce dataset** with 24 columns
- Handled missing values, removed ₹ symbols, filtered by rating ≥ 4.0
- Created derived column `total_amount = final_price × ratings_count`
- Exported clean data as `Combined_dataset_CLEANED.csv`

### 📌 Week 02 — SQL Sales Analysis (ShopEase DB)
- Built a relational database from scratch with **4 tables, 27 queries**
- Covered SQL Basics → Filtering → Aggregation → Joins → Transactions
- Demonstrated ACID properties with real BEGIN/COMMIT/ROLLBACK transactions
- Used CASE statements, HAVING, indexes, and SARGable query rewrites

### 📌 Week 03 — Advanced SQL (Superstore)
- Analyzed **9,994 rows** of Superstore sales data
- Applied correlated subqueries, CTEs, and 3 types of window functions
- Identified top customer **Sean Miller (₹25,043)** and churn risks (12 single-order customers)
- Built a final combined query using **JOIN + CTE + DENSE_RANK()** together


### 📌 Week 04 — Azure Cloud & ADF Pipeline
- Provisioned end-to-end Azure infrastructure: Resource Group → Storage Account → Blob Containers
- Uploaded Sample Superstore CSV as source data in Blob Storage
- Built ADF pipeline pl_CopySuperstoreData with Get Metadata + Copy Data activities
- Validated file metadata (itemName, size, columnCount) before triggering data copy
- Successfully copied data to destination container — output_superstore.csv 
- Implemented RBAC with Reader, Contributor, and Storage Blob Data Contributor roles

 ### 📌 Week 5 Spark Assignment 
 
- Set up an Apache Spark (PySpark) environment and loaded a 1000-row e-commerce dataset into Spark DataFrames.
- Cleaned real-world messy data by removing duplicates, handling null values, filling missing fields, and filtering invalid records.
- Applied DataFrame transformations such as filtering, renaming columns, type casting, and selecting relevant data.
- Performed aggregations using count(), sum(), avg(), min(), and max(), along with groupBy() operations.
- Built a complete Spark pipeline combining data cleaning, transformation, and revenue aggregation by store.
---
## 📊 Skills Gained So Far

| Category | Skills |
|---|---|
| 🐍 Python | Pandas, Data Cleaning, EDA, Data Transformation |
| 🗄️ SQL — DDL | CREATE, DROP, ALTER, Constraints |
| 📝 SQL — DML | INSERT, UPDATE, DELETE |
| 🔍 SQL — Queries | SELECT, JOINs, Subqueries, CTEs, HAVING |
| 🪟 Window Functions | RANK(), DENSE_RANK(), ROW_NUMBER(), PARTITION BY |
| 🔐 Transactions | ACID Properties, BEGIN, COMMIT, ROLLBACK |
|☁️ Azure Cloud | Resource Groups, Blob Storage, Storage Accounts, IAM |
|🔄ADF (ETL)| Linked Services, Datasets, Pipelines, Get Metadata, Copy Data|
|🔑 Security| RBAC, Managed Identity, Role Assignments, PoLP|
|⚡ Apache Spark (PySpark)|	SparkSession, DataFrames, Distributed Processing, In-Memory Computing|
|🧹 Data Processing|	Data Cleaning, Deduplication, Null Handling, Data Validation|
|🔄 Data Transformation|	Filtering, Column Renaming, Type Casting, DataFrame Transformations|
|📊 Data Analysis|	Aggregations (SUM, AVG, MIN, MAX, COUNT), GroupBy Operations|
|⚙️ Big Data Concepts|	MapReduce vs Spark, Narrow & Wide Transformations, Shuffle Operations|
|🚀 ETL Pipelines	|End-to-End Data Cleaning, Transformation, Aggregation Workflows|
---

## 🧠 Learnings & Reflections

- Learned why **correlated subqueries are slow** and how CTEs are a cleaner alternative
- Understood the real difference between **RANK() vs DENSE_RANK()** through hands-on queries
- Realized how **window functions preserve row-level detail** while still doing aggregations
- Appreciated how **good database design** (normalized tables) makes queries faster and cleaner
- Grew comfortable reading and writing **production-style SQL** with proper comments
- Understood how Azure Resource Groups act as logical boundaries for cost and access management
- Learned how ADF Linked Services decouple connection logic from pipeline logic
- Experienced how metadata-driven pipelines make ETL workflows dynamic and fault-tolerant
- Applied Principle of Least Privilege using Azure IAM role assignments in a real cloud environment
- Developed a strong understanding of Apache Spark's DataFrame operations, including data cleaning, transformation, aggregation, and building efficient data-processing pipelines on large datasets.
- This assignment provided practical experience in handling real-world messy data and demonstrated how proper data cleaning and transformation are essential for producing accurate and meaningful analytical results

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Azure Data Factory](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=flat&logo=microsoft-azure&logoColor=white)

---

## 📬 Connect With Me
Feel free to connect if you're also on this journey or want to discuss data engineering!

⭐ **Star this repo** if you find it helpful — it motivates me to keep going!




