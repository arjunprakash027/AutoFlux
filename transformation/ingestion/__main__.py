"""
Author : Arjun P
Modified on : 11/02
"""

from statistella_ingest import download_train_test
from utils import traverse_folder, ingest_spark

if __name__ == '__main__':
    download_train_test()
    files = traverse_folder(
        dir = 'datasets'
    )

    ingest_spark(
        files=files
    )

    