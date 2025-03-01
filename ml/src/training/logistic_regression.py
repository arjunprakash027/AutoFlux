# Internal imports
from src import build_spark
spark = build_spark()
from src.utils.traditional_ml.trainer import Trainer

# Library imports
import mlflow
import mlflow.sklearn
#sklearn imports
from sklearn.linear_model import LogisticRegression
#pandas imports
from pandas import DataFrame


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
