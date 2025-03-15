# Imports
from src.utils.config_reader import PredictorConfigrations
import mlflow.pyfunc
import mlflow
import numpy as np
import pandas as pd

class Predictor:
    
    def __init__(self,config:PredictorConfigrations):
        
        self.config = config
    
    def _build_mlflow(self) -> None:
        mlflow.set_tracking_uri("http://0.0.0.0:6969")

    def _build_predictor(self) -> None:
        
        # Let the class know where to pick the model from
        self._build_mlflow()

        model_name = self.config.registered_model
        model_version = self.config.version

        model = mlflow.pyfunc.load_model(
            model_uri = f"models:/{model_name}/{model_version}"
        )

        self.model = model

    def predict(self, df:pd.DataFrame) -> np.array:
        
        self._build_predictor()
        out = self.model.predict(df)

        return out