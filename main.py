from typing import List
from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import schedule
import time
import os
from google.cloud import storage

app = FastAPI()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'aerial-velocity-359918-e385a21f34a1.json'
storage_client = storage.Client()
bucket_name = 'pi2-catraca'

class Pickle(BaseModel):
    encodings: List[List[float]]
    names: List[str]

def dowload_pickle(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        print('true')
        return True
    except Exception as e:
        print(e)
        return False

schedule.every(0).minutes.do(dowload_pickle, 'encodings.pickle', os.path.join(os.getcwd(), 'encodings.pickle'), bucket_name)

while True:
    schedule.run_pending()
    time.sleep(60)