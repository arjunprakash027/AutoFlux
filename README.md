# AutoFlux
A end to end workflow to run ingestion of data to pre-processing to training to deployment of an ML model

For more indepth docs on particular services:

*** This is lite version of the setup and in active development ***
*** For spark version (not in active development) change the branch to main ***

[ML](/ml/README.md) 

[Ingestion & Transformation](/transformation/README.md)

A very basic architecture of environment setup using AutoFlux
![AutoFlux v0 1 architecture](https://github.com/user-attachments/assets/bc4849ff-8a67-4421-8996-2bad0633db1b)


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

