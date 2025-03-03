# AutoFlux
A end to end workflow to run ingestion of data to pre-processing to training to deployment of an ML model

For more indepth docs on particular services:

[ML](/ml/README.md)
[Ingestion & Transformation](/transformation/README.md)

A very basic architecture of environment setup using AutoFlux
![AutoFlux v0 1 architecture](https://github.com/user-attachments/assets/bc4849ff-8a67-4421-8996-2bad0633db1b)

# Apache Spark + Hive + Delta Lake + PostgreSQL Metastore

### **A Basic Distributed Data Processing Architecture**

This project sets up **Apache Spark with Hive**, using **PostgreSQL as the Hive Metastore**, and **Delta Lake for data storage**. It provides an **SQL queryable data warehouse** while leveraging Spark’s processing power for analytics.

> **⚠ Warning:**  
> This is a **basic setup** to get Spark, Hive, and Delta Lake working together. It is **not production-ready** and does not include:
> 
> - **Security (Authentication & Authorization)**
> - **Performance optimizations**
> - **High Availability**
> - **Advanced Storage Configurations (e.g., S3, HDFS)**
> 
> Future improvements can include **Kubernetes deployment, caching strategies, and access control policies**.

---

## **Architecture Overview**

### **Components & Responsibilities**

| **Component**             | **Purpose**                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| **Spark Master**          | Orchestrates Spark jobs, manages cluster resources                                       |
| **Spark Worker(s)**       | Executes Spark tasks distributedly                                                       |
| **Hive Metastore**        | Stores metadata (table schema, partitions, etc.)                                         |
| **PostgreSQL**            | Stores Hive Metastore information (instead of Derby)                                     |
| **Delta Lake**            | Provides ACID transactions and schema enforcement for Spark tables                       |
| **Thrift Server**         | Exposes an SQL endpoint for BI tools (JDBC/ODBC)                                         |
| **DBT (Data Build Tool)** | Helps transform and manage data using SQL                                                |
| ML container              | For running python, pyspark and ML workloads in distributed (using spark) and local mode |

---

### **How Everything Comes Together**

When we launch all Docker containers using `restart_compose.sh`, the entire pipeline comes to life. This includes the Spark master, Spark worker, Hive metastore, Postgres server, transformation server, and ML server.

- The **transformation server** handles data ingestion from various sources (custom code) and stores it in **Delta Lake**.
- **Transformation scripts** (written in SQL within DBT) then process and transform this data, again storing the output in **Delta Lake**. This is achieved using **PySpark** and **Thrift connections** via DBT.
- The **Hive metastore**, running inside the Postgres container, manages metadata for tables and schemas and is connected to the Spark master.
- All **Spark jobs** are executed through the Spark master in the **Heavy version** (whereas in the **Lite version**, there’s no Spark master—only PySpark within the ML container for development).

On the **ML side**, the ML container has all necessary dependencies installed. It fetches data from **Delta Lake via PySpark**, converts it into a **Pandas DataFrame**, and runs **ML algorithms** on it. The entire ML pipeline is tracked using **MLflow**, and its UI can be accessed at `localhost:6969` for monitoring

## **🔧 How to Set Up & Run**

### **1️⃣ Prerequisites**

Ensure you have:

- **Docker** installed
- **Docker Compose** installed

### **2️⃣ Clone the Repository**

```bash
git clone https://github.com/arjunprakash027/AutoFlux.git
```

### **3️⃣ Start the Docker Containers**

```bash
docker-compose up -d
```

> This will start **Spark, Hive, PostgreSQL, Thrift Server, and Delta Lake**.

---

## **What does each container do**
### **Hive Metastore  (hive-metastore) container** 

- Stores metadata about tables, schemas, and partitions.
- Uses **PostgreSQL as its backend** instead of Derby.
- Exposes a **Thrift service** (`thrift://metastore-db:9083`) for external connections.

### **Apache Spark (spark-master, spark-worker) container**

- **Spark Master**: Manages job scheduling and resource allocation runs on port 7077.
- **Spark Workers**: Execute Spark tasks.
- Exposes SQL interface using thrift server at 10000 port for dbt
- PySpark on ML container can connect directly to port 7077 as it uses session

### **Delta Lake volume**

- Provides **ACID transactions** and **schema enforcement** for Spark.
- Stores data in **Parquet format** with **transaction logs**.
- Is mounted as a volume to every container that needs it mimicking an cloud container in S3
- Future plan is to use MiniO server for delta lake

### **DBT (Data Build Tool) container**

- Transforms raw data using SQL.
- Connects to the **Thrift Server** for querying.

### **Machine Learning container**

- To perform ML based and python workloads 
- Uses PySpark and connects directly to spark on port 7077 to execute spark workloads
---

## **Step-by-Step Usage**

### **Bring everything up**

```bash
bash restart_compsose.sh
```
Will build and run every container

### **Verify the Setup**

Check that all containers are running:

```bash
docker ps
```

You should see:

![image](https://github.com/user-attachments/assets/184686ef-51ec-4726-a8f6-b26583e92b8a)

### **Run transformation**

```bash
docker exec -it transformation bash
```
You'll get access to a transformation container where you can execute DBT commands. By default, the `seed` command runs automatically, and you can trigger the transformation process using `dbt build`, which will execute everything.

### **3️⃣ Run PySpark with Hive Support**

```python
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (
    SparkSession.builder
    .appName("PySparkWithStandaloneMetastore")
    .master("spark://spark-master:7077")
    .config("hive.metastore.uris", "thrift://metastore-db:9083")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark = builder.enableHiveSupport().getOrCreate()

print(spark.sql("SHOW DATABASES").show())
```

Run this code inside ml container too see all the databases and query them when needed. Data will be stored in delta lake and metadata will be stored in postages using hive as metastore manager

---

## **Stopping the Containers**

To stop the entire setup:

```bash
docker-compose down
```

To remove all volumes and networks:

```bash
docker-compose down -v
```

---

