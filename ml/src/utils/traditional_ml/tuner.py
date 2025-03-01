from abc import abstractmethod, ABC
import pandas as pd

#Sklearn imports
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import HalvingGridSearchCV

class BaseTuner(ABC):

    def __init__(self,
                 model,
                 X_train:pd.DataFrame,
                 y_train:pd.DataFrame,
                 X_test:pd.DataFrame,
                 y_test:pd.DataFrame,
                 params:dict) -> None:
        
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.params = params

    @abstractmethod
    def tune(self):
        "Inheriting classes should implement this method"
        pass


class GridSearchTuner(BaseTuner):

    def tune(self) -> dict:

        print(f"Model: {self.model}")
        grid = HalvingGridSearchCV(
            self.model,
            self.params,
            factor=2,
            resource='n_samples',
            min_resources='exhaust',
            max_resources=len(self.X_train),
            scoring="f1",
            cv=8,
            n_jobs=-1,
            verbose=3
        )

        grid.fit(self.X_train, self.y_train)

        return grid.best_params_

class TunerFactory(BaseTuner):

    def tune(self) -> dict:
        
        print(f"Model: {self.model}")
        tuned_params = GridSearchTuner(
            self.model,
            self.X_train,
            self.y_train,
            self.X_test,
            self.y_test,
            self.params
        ).tune()

        return tuned_params