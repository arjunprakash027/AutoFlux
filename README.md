# AutoFlux-lite
A end to end workflow to run ingestion of data to pre-processing to training to deployment of an ML model

For more indepth docs on particular services:

***This is lite version of the setup and in active development***

***For the spark version (not in active development) change the branch to main***

[ML](/ml/README.md) 

[Ingestion & Transformation](/transformation/README.md)

A very basic architecture of environment setup using AutoFlux-lite
![AutoFlux Lite Architecture](https://github.com/user-attachments/assets/f8f2339f-d954-43b1-8e66-53f06065d03b)


## Overview of the architecture

This is a lightweight version of a larger architecture that originally involved Spark, Hive, PostgreSQL, and Delta Lake. Instead of relying on these heavyweight components, this version leverages DuckDB—an embedded OLAP database—for efficient data storage and processing while keeping the system low on power consumption and compute requirements.

### How It Works (Refer to the Architecture Diagram)

#### 1.	Transformation & Ingestion:
•	Raw data is ingested and processed inside the dbt container.
•	After transformation, the cleaned data is stored in DuckDB, acting as the shared storage layer.
#### 2.	Machine Learning Pipeline:
•	The ML container fetches the transformed data from DuckDB.
•	Data is further cleaned and preprocessed inside the ML container.
•	MLflow is used to:
•	Track experiments.
•	Log metrics and artifacts.
•	Store model versions for reproducibility.
#### 3.	Outputs:
•	A model accuracy and experiment dashboard for evaluation.
•	A final trained model artifact ready for deployment.

This setup is ideal for environments with limited compute resources, making it accessible for local development, edge devices, and low-power machines while maintaining an efficient ML pipeline.

## **Step-by-Step Usage**

### **Bring everything up**

```bash
bash compose_build.sh
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

