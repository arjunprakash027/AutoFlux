"""
Author : Arjun P
Modified on : 11/02
"""
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

def download_train_test() -> None:
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('veryvarg/statistella-data-analytics',path='datasets',unzip=True)    
