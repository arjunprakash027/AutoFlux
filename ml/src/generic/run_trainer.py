# Internal imports
import sklearn.linear_model
from src.utils.config_reader import read_config, Configrations
from src.utils.traditional_ml.trainer import Trainer

# Library imports
# sklearn imports
import lightgbm
import sklearn
#pandas imports
import pandas as pd
import ibis
import duckdb

class TrainerPipeline:

    def __init__(self,config:Configrations, df:pd.DataFrame):
        self.config:Configrations = config
        self.df = df
    
    @property
    def model_map(self) -> dict:

        return {
            "LogisticRegression": sklearn.linear_model.LogisticRegression,
            "LGBMClassifier": lightgbm.LGBMClassifier
        }

    def _trainer_flow(self) -> None:
        
        target = self.config.training.target

        models = self.config.models

        for model,params in models.items():

            model_class = self.model_map.get(model,None)

            if not model_class:
                print(f"Model not supported yet!")
                continue
            
            params = params.model_params

            trainer = Trainer(
                estimator=model_class,
                df = self.df,
                target=target,
                params=params,
                hyper_params_config=self.config.hyper_parameter_tuning
            )

            trainer.fit()

    def pipeline_run(self):
        self._trainer_flow()

if __name__ == "__main__":
    pass