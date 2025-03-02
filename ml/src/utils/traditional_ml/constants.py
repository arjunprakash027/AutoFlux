from dataclasses import dataclass
from typing import Dict,Any

@dataclass
class ParamSpace:

    param_space: Dict[str,Dict[str,Any]] = None

    def __post_init__(self):

        self.param_space = {

            "LogisticRegression": {
                "penalty": ["l1","l2","elasticnet","none"],
                "C": [0.1,1,10,100],
                "solver": ["newton-cg","lbfgs","liblinear","sag","saga"],
                "max_iter": [100,500,1000,5000]
            },
            "LGBMClassifier": {
                "objective": ["binary"],
                "boosting_type": ["gbdt","dart"],
                #"max_depth": [10,50,100,500],
                #"n_estimators": [100,500,1000,5000],
                #"num_leaves": [31,127,511,2047],
                #"learning_rate": [0.1,0.01,0.001,0.0001],
                "is_unbalance": [True],
            },
            "xgboost": {
                "objective": ["binary:logistic"],
                "booster": ["gbtree","gblinear","dart"],
                "max_depth": [10,50,100,500],
                "n_estimators": [100,500,1000,5000]
            },
            "random_forest": {
                "n_estimators": [100,500,1000,5000],
                "max_depth": [10,50,100,500],
                "criterion": ["gini","entropy"],
                "max_features": ["auto","sqrt","log2"]
            }
        }
    
    def get_param_space(
            self,
            model_name:str
    ) -> Dict[str,Any]:
        
        return self.param_space.get(model_name,None)