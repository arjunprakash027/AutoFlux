# ML workflow for AutoFlux

**Version:** 0.0.1  

## **Prerequisites**
Before running AutoFlux, ensure the following dependencies and services are up and running:
- **Poetry** is installed for dependency management. (Done in ml container)
- **MLflow Server** is running on port **6969**. (Done in ml contianer)

## **1️⃣ Configuring `ml-compose.yaml`**
The **ml-compose.yaml** file is crucial for setting up model training. You can find it inside the **src/** directory.  

Before running the pipeline, modify the necessary configurations:

### **General Configuration**
- **`input_data_source`**: Specify the schema and table name for training data in duckdb (**`schema.table_name`** format).  
- **`target`**: Define the target variable for supervised learning.  
- **`unique_identifier`** *(optional)*: Set the column used as a unique ID (e.g., `customer_id`).

### **Model Selection**
Under the `models` section, define the models to be trained.  
- Currently supported models: **LightGBM** and **Logistic Regression**.  
- Each model has **hyperparameters** defined in `model_params`. Modify these as needed.

#### **Example `ml-compose.yaml` Configuration**
```yaml
project_name: AutoFlux

training:
  input_data_source: default_staging.stg_full
  target: TARGET

models:
  LGBMClassifier:
    experiment_name: lightgbm_experiment
    model_params:
      boosting_type: gbdt
      num_leaves: 31
      max_depth: -1
      learning_rate: 0.1
      n_estimators: 100
      class_weight: balanced

  LogisticRegression:
    model_params:
      penalty: l2
      C: 1.0
      solver: lbfgs
      class_weight: balanced
      max_iter: 100
```

---

## **2️⃣ Hyperparameter Tuning Configuration**
AutoFlux supports **Halving Grid Search** for hyperparameter tuning.

Modify the `hyper_parameter_tuning` section in `ml-compose.yaml`:
```yaml
hyper_parameter_tuning:
  perform: True    # Set to False if no hyperparameter tuning is required.
  scoring: f1      # Scoring metric (e.g., accuracy, precision, recall).
  cv: 5            # Number of cross-validation folds.
  factor: 2        # Reduction factor for Halving Grid Search.
```
> More tuning strategies will be introduced in future versions.

---

## **3️⃣ Running the Training Pipeline**
### **Trainer File: `run_trainer.py`**
- The **Trainer pipeline** (`run_trainer.py`) orchestrates the training process.
- It automatically selects and trains models based on the **ml-compose.yaml** configuration.
- It supports multiple models and iterates through each to train them.

### **Steps to Run the Pipeline**
1. Ensure all services are running (**MLflow, duckdb, PostgreSQL**).
2. Get into the docker container:
   ```bash
   docker exec -it ml bash
   ```
3. Run the trainer:
   ```bash
   python -m src.training.run_trainer
   ```
4. View experiment logs in **MLflow UI**:
   navigate to localhost:6969

---

## **4️⃣ Utilities and Supporting Modules**
### **Config Reader (`config_reader.py`)**
- Uses **Pydantic** to validate and parse `ml-compose.yaml`.  
- Ensures that at least one model is defined before training.  
- Can be modified if custom configurations are required.

### **Trainer (`trainer.py`)**
- Handles **data preprocessing, model training, and MLflow logging**.
- Supports:
  - **Automatic logging** of all hyperparameters and feature importance.
  - **Global MLflow module** for centralized experiment tracking.
  - Custom logging inside the `fit` function.

### **Tuner (`tuner.py`)**
- Implements **hyperparameter tuning** with **Halving Grid Search**.
- `BaseTuner` is the abstract class for all tuning methods.
- `TunerFactory` is used to select and run tuning strategies.

---

## **5️⃣ MLflow Integration**
All model training and tuning logs are stored in **MLflow** for easy tracking.  
- The **MLflow server** is started at `http://0.0.0.0:6969`.  
- **Logged Artifacts**:
  - **Feature Importance** (Logged as JSON)
  - **Hyperparameters** (Logged in `hyperparameters.json`)
  - **Performance Metrics** (Accuracy, F1-score, Precision, Recall)

---

## **6️⃣ Deployment via Docker**
To run AutoFlux in a **Dockerized environment**, use the provided `Dockerfile`.