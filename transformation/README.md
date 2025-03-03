# Transformation & Ingestion in AutoFlux

AutoFlux integrates **Spark, Hive, PostgreSQL, Delta Lake, and dbt** for scalable and efficient **data ingestion and transformation** before ML model training.  

This module ensures that raw data is **ingested, cleaned, and transformed** before being used in the ML pipeline.  


## **1️⃣ Data Ingestion**
The **ingestion process** ensures that data is loaded into **Spark** and stored in **Delta Lake** for further transformation.

### **📌 Ingestion Script Overview**
The ingestion script is located in:
```
transformation/ingestion/
```
- **`statistella_ingest.py`** → Downloads datasets (supports **Kaggle**).  
- **`utils.py`** → Contains helper functions for **traversing folders** and **ingesting into Spark**.  
- **`__main__.py`** → Runs the ingestion pipeline.  

### **🚀 Running the Ingestion Script**
To run the ingestion process, execute:
```bash
python -m ingestion
```
This will:
1. **Download datasets** from Kaggle (if configured).  
2. **Scan the dataset directory** for files.  
3. **Load files into Spark** and store them in **Delta Lake** under the `raw` schema.  

> **Customize `ingest_spark()`** in `utils.py` if you need a different ingestion process.  

---

## **2️⃣ Transformation using dbt**
Once data is ingested into Spark, **dbt** handles **data transformation** into clean, structured datasets.

### **📌 Key Configuration Files**
- **`profiles.yml`** → Configures dbt to connect to **Spark** (or another database if needed).  
- **`dbt_project.yml`** → Defines the dbt project structure.  
- **`models/sources.yml`** → Specifies raw data sources.  
- **`models/staging/`** → Contains statging logic.  

### **💡 Customizing dbt for Your Needs**
1. **Change Data Source**  
   - Modify **`sources.yml`** to update input tables.  
   - Example:
     ```yaml
     sources:      
       - name: input_data
         schema: raw
         tables:
           - name: test
           - name: train
     ```

2. **Write Custom Staging & Transformation Logic**  
   - Use `stg_train.sql` and `stg_test.sql` in `models/staging/` to define **staging transformations**.  
   - Modify **`stg_full.sql`** to **merge datasets** as required.

3. **Configure `profiles.yml` for a Different DB**  
   - If **Spark is not your preference**, modify `profiles.yml` to point to another database (e.g., PostgreSQL, BigQuery).  

### **🚀 Running the dbt Transformation**
Once ingestion is complete, run:
```bash
dbt run
```
This will:
1. Load data into **staging tables**.
2. Apply **transformations** (joins, filtering, feature engineering).
3. Store the final dataset **back in Spark** for ML model training.

---

## **3️⃣ Integration with ML Container**
After transformation, the ML pipeline (**AutoFlux**) reads the processed data from Spark.

### **📌 Steps**
1. **Ingest raw data** → Stored in **Delta Lake (`raw` schema)**.  
2. **Run dbt transformations** → Output stored in **staging/mart schemas**.  
3. **ML container reads the transformed data** for model training.  

💡 **Ensure that the ML container is set up to read data from the correct schema/table.**  