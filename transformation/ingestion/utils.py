"""
Author : Arjun P
"""

from pathlib import Path
from typing import List
import pandas as pd
import duckdb

def traverse_folder(dir:str) -> List:
    
    return [f"{dir}/{f.name}" for f in Path(dir).iterdir() if f.is_file()]

def ingest_duckdb(
        files: List
) -> None:
    
    con = duckdb.connect("database/ml_db.duckdb")
    print("Connection Type:", con.execute("PRAGMA database_list;").fetchall())

    # Duckdb expects schemas to be present before writing to it
    schema_name = "raw"
    con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
     
    for file in files:
        try:
            table_name = f"{schema_name}.{file.split('/')[-1].split('.')[0]}"
            con.execute(
                f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file}', header=True);"
            )
            print(f"{table_name} table created in duckdb!")
        except Exception as e:
            print(e)
