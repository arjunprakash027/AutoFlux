"""
Author : Arjun P
Modified on : 11/02
"""

from statistella_ingest import download_train_test
from utils import traverse_folder, ingest_duckdb

if __name__ == '__main__':
    
    # Download the dataset using this code
    download_train_test()
    
    # Setup files and duckdb 
    files = traverse_folder(
        dir = 'datasets'
    )
    print(files)
    import duckdb
    con = duckdb.connect("database/ml_db.duckdb")
    
    # Ingest the data into duckdb using this code 
    ingest_duckdb(
        files=files
    )

    