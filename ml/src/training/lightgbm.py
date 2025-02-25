# Internal imports
from src import build_spark
spark = build_spark()
from src.training.utils import Trainer

# Library imports
import mlflow
import mlflow.sklearn
#sklearn imports
import lightgbm as lgb
#pandas imports
from pandas import DataFrame

# Setting up mlflow

df:DataFrame = spark.read.table("default_staging.stg_full").limit(10000).toPandas()
df_num = df.select_dtypes(include=['number'])
df_num = df_num.fillna(0)

params = {
    "objective": "binary",
    "boosting_type": "dart",
    "max_depth": 1000,
    "n_estimators": 100
}

trainer = Trainer(
    estimator=lgb.LGBMClassifier,
    df=df_num,
    target="TARGET",
    params=params
)

trainer.fit()