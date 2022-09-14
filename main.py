from typing import List
from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import schedule
import time
import os
from google.cloud import storage
from sqlalchemy import null

app = FastAPI()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'aerial-velocity-359918-e385a21f34a1.json'
storage_client = storage.Client()
bucket_name_pickle = 'pi2-catraca'
bucket_name_biometria = 'biometria-pi2'

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

def list_file(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    files = []

    for blob in blobs:
        files.append((blob_metadata(bucket_name_biometria, blob.name)))

    return files

def blob_metadata(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    return {'file': blob.name, 'bucket': blob.bucket.name, 'updated': blob.updated}
    
def last_file(file1, file2):
    return

def dateFile(date):
  return date['updated']

files = list_file(bucket_name_biometria)

files.sort(key=dateFile, reverse=True)

schedule.every(0).minutes.do(dowload_pickle, 'encodings.pickle', os.path.join(os.getcwd(), 'encodings.pickle'), bucket_name_pickle)
schedule.every(0).minutes.do(dowload_pickle, files[0]['file'], os.path.join(os.getcwd(), './biometria/{nome}').format(nome = files[0]['file']), bucket_name_biometria)

while True:
    schedule.run_pending()
    time.sleep(60)