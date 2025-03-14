from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pandas import DataFrame
import mlflow
import mlflow.sklearn

#internal imports
from src.utils.traditional_ml.tuner import TunerFactory
from src.utils.config_reader import HyperParameterBaseModel

class Trainer:
    def __init__(self, 
                 estimator, #the estimator can be any model -> should type safe it later
                 df:DataFrame,
                 target:str,
                 params:dict,
                 experiment_name:str = None,
                 tag:str = "default tag",
                 hyper_params_config:HyperParameterBaseModel = HyperParameterBaseModel) -> None:
        
        # ml flow settings
        self.estimator_name = estimator.__name__
        self.experiment_name = experiment_name if experiment_name else self.estimator_name
        self.tag = tag

        # Configs
        self.hyper_params_config = hyper_params_config

        # ml model settings
        self.estimator = estimator
        self.target = target        
        self.params = params

        self.X = df.drop(target,axis=1)
        self.y = df[target]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2
        )

        self._y_pred = None
        self._accuracy_metrices = None

    @property
    def y_pred(self):
        if self._y_pred is None:
            raise ValueError("Model not yet fitted")
        return self._y_pred
    
    @y_pred.setter
    def y_pred(self, value):
        self._y_pred = value

    @property
    def accuracy_metrices(self):
        if self._accuracy_metrices is None:
            raise ValueError("Model not yet fitted")
        return self._accuracy_metrices
    
    @accuracy_metrices.setter
    def accuracy_metrices(self,value):
        self._accuracy_metrices = value

    def _get_model_feature_mapping(self) -> dict:
        
        """
        Just gets the feature importance value of certain set of estimators
        """
        if self.estimator_name in ["LogisticRegression","LinearRegression"]:
            return dict(
                zip(
                    self.X.columns,
                    self.estimator.coef_[0]
                )
            )
        
        elif self.estimator_name in ["LGBMClassifier","LGBMRegressor",
                                    "XGBClassifier","XGBRegressor",
                                    "RandomForestClassifier","RandomForestRegressor"]:
            return dict(
                zip(
                    self.X.columns,
                    self.estimator.feature_importances_
                )
            )
        
        else:
            return dict(
                zip(
                    self.X.columns,
                    [0 * len(self.X.columns)] # we do not know the feature importance of this model
                )
            )
        

    def fit(self) -> None:
        # the entire training process is in here to easily log whatever we want in mlflow
    
        mlflow.set_tracking_uri("http://0.0.0.0:6969")
        mlflow.set_experiment(self.experiment_name)
        mlflow.set_tag("tag", self.tag)
        
        #Enable individual autologs
        mlflow.sklearn.autolog()
        mlflow.lightgbm.autolog()
        
        # Tune hyper parameters
        if self.hyper_params_config.perform:
            tuner = TunerFactory(
                model=self.estimator(),
                model_name=self.estimator_name,
                X_train=self.X_train,
                y_train=self.y_train,
                X_test=self.X_test,
                y_test=self.y_test,
                hyper_params_config=self.hyper_params_config
            )
            self.params = tuner.tune()

        #fit the estimator based on received hyperparameters
        self.estimator = self.estimator(**self.params)
        self.estimator.fit(self.X_train, self.y_train)

        self.y_pred = self.estimator.predict(self.X_test)
        self.self_test = self.estimator.predict(self.X_train)

        self.accuracy_metrices = {
            "accuracy_test": accuracy_score(self.y_test, self.y_pred),
            "accuracy_train": accuracy_score(self.y_train, self.self_test),
            "precision_test": precision_score(self.y_test, self.y_pred),
            "precision_train": precision_score(self.y_train, self.self_test),
            "recall_test":recall_score(self.y_test, self.y_pred),
            "recall_train":recall_score(self.y_train, self.self_test),
            "f1_test":f1_score(self.y_test, self.y_pred),
            "f1_train":f1_score(self.y_train, self.self_test)
        }


        for metric, value in self.accuracy_metrices.items():
            mlflow.log_metric(metric, value)
        
        feature_importance = self._get_model_feature_mapping()
        
        # Logging neccessary artifacts
        mlflow.log_dict(feature_importance, "feature_importance.json")
        mlflow.log_dict(self.params, "hyperparameters.json")
        
        mlflow.end_run()