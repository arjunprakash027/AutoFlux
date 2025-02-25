# Internal imports
from src import build_spark
spark = build_spark()
from src.training.utils import Trainer

# Library imports
import mlflow
import mlflow.sklearn
#sklearn imports
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
#pandas imports
from pandas import DataFrame

# Setting up mlflow

df:DataFrame = spark.read.table("default_staging.stg_full").limit(1000).toPandas()
df_num = df.select_dtypes(include=['number'])
df_num = df_num.fillna(0)

params = {
    "solver":"lbfgs",
    "random_state":42,
    "class_weight":"balanced",
    "max_iter":10000
}

trainer = Trainer(
    estimator=LogisticRegression,
    df=df_num,
    target="TARGET",
    params=params
)

trainer.fit()

