import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict,Any,Optional
from pydantic import BaseModel, Field, model_validator


class ModelBase(BaseModel):
    experiment_name: str = Field(None)
    model_params: Optional[Dict[str,Any]] = Field({}, description="Model parameters")
 
class TrainingBaseModel(BaseModel):
    input_data_source: str = Field(...,description="Input data source")
    target: str = Field(...,description="Target value")
    unique_identifier: str = Field(None,description="Unique identifer of each row")

class HyperParameterBaseModel(BaseModel):
    perform: bool = Field(False)
    scoring: str = Field(...)
    cv: int = Field(...)
    factor: int = Field(...)

class Configrations(BaseModel):
    project_name: str = Field("Default")
    training: TrainingBaseModel
    models: Dict[str, ModelBase]
    hyper_parameter_tuning: HyperParameterBaseModel

    @model_validator(mode="before")
    @classmethod
    def validate(cls,values:Any) -> Any:
        cls._validate_models(values=values)
        return values

    @classmethod
    def _validate_models(cls,values:Any) -> Any:
        "Ensure atleast there is one model"

        if not values.get("models"):
            raise ValueError("There should be atlest one model for training!")
        
        for model_name,params in values.get("models").items():
            if not params:
                values['models'][model_name] = {"model_params":{}} # Ensure model_params are present always

class InputDefiner:
    def __init__(self, config_path: Path):
        self.config_path = config_path
    
    def _read_config(self) -> Dict[str,Any]:
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def return_config_dataclass(self) -> Configrations:
        config = self._read_config()
        return Configrations(**config)
        #return Configrations(**config)


def read_config() -> Configrations:
    return InputDefiner(Path("src/ml-compose.yaml")).return_config_dataclass()


if __name__ == "__main__":
    print(read_config())

