from abc import abstractmethod, ABC
import pandas as pd

#Sklearn imports
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV

#Internal imports
from src.utils.traditional_ml.constants import ParamSpace
from src.utils.config_reader import HyperParameterBaseModel

class BaseTuner(ABC):

    def __init__(self,
                 model,
                 model_name:str,
                 X_train:pd.DataFrame,
                 y_train:pd.DataFrame,
                 X_test:pd.DataFrame,
                 y_test:pd.DataFrame,
                 hyper_params_config: HyperParameterBaseModel = HyperParameterBaseModel,
                 params:dict = None) -> None: #Input can be none only for Tuner Factory
        
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.params = params
        self.model_name = model_name

        #configs
        self.hyper_params_config = hyper_params_config

    @abstractmethod
    def tune(self):
        "Inheriting classes should implement this method"
        pass


class GridSearchTuner(BaseTuner):

    def tune(self) -> dict:

        scoring = self.hyper_params_config.scoring
        cv = self.hyper_params_config.cv
        factor = self.hyper_params_config.factor

        grid = HalvingGridSearchCV(
            self.model,
            self.params,
            factor=factor,
            resource='n_samples',
            min_resources='exhaust',
            max_resources=len(self.X_train),
            scoring=scoring,
            cv=cv,
            n_jobs=-1,
            verbose=3
        )

        grid.fit(self.X_train, self.y_train)

        return grid.best_params_

class TunerFactory(BaseTuner):

    def tune(self) -> dict:
        
        print(f"Fine tuning: {self.model_name}")

        if not self.params:
            self.params = ParamSpace().get_param_space(self.model_name)

        tuned_params = GridSearchTuner(
            self.model,
            self.model_name,
            self.X_train,
            self.y_train,
            self.X_test,
            self.y_test,
            self.params,
            hyper_params_config=self.hyper_params_config
        ).tune()

        return tuned_params