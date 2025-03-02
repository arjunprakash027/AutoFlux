# Internal imports
import sklearn.linear_model
from src.utils.config_reader import read_config, Configrations
from src.utils.traditional_ml.trainer import Trainer

from src import build_spark
spark = build_spark()
from src.utils.traditional_ml.trainer import Trainer

# Library imports
# sklearn imports
import lightgbm
import sklearn
#pandas imports
from pandas import DataFrame

class TrainerPipeline:

    def __init__(self,config:Configrations):
        self.config:Configrations = config
    
    @property
    def model_map(self) -> dict:

        return {
            "LogisticRegression": sklearn.linear_model.LogisticRegression,
            "LBGMClassifier": lightgbm.LGBMClassifier
        }
    
    def _read_input(self) -> None:
        
        """
        Input table retreival flow -> write any custom input table code here
        """
        input_table = self.config.training.input_data_source

        df:DataFrame = spark.read.table(input_table).limit(10000).toPandas()
        df_num = df.select_dtypes(include=['number'])
        df_num = df_num.fillna(0)

        self.df = df_num # Assign your final transformed table here

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

    def _pipeline_run(self):

        self._read_input()
        self._trainer_flow()

if __name__ == "__main__":
    
    config = read_config()

    trainer = TrainerPipeline(config=config)

    trainer._pipeline_run()

# params = {
#     "objective": "binary",
#     "boosting_type": "dart",
#     "max_depth": 1000,
#     "n_estimators": 100
# }

# trainer = Trainer(
#     estimator=lgb.LGBMClassifier,
#     df=df_num,
#     target="TARGET",
#     params=params
# )

# trainer.fit()