"""
Author : Arjun P
Modified on : 11/02
"""

from statistella_ingest import download_train_test
from utils import traverse_folder, ingest_duckdb

if __name__ == '__main__':
    pass
    # download_train_test()
    files = traverse_folder(
        dir = 'datasets'
    )
        
    print(files)

    import duckdb
    con = duckdb.connect("database/ml_db.duckdb")

    # ingest_duckdb(
    #     files=files
    # )

    