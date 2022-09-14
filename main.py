from datetime import date, datetime
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
lastDat = null
lastPicke = null

class Pickle(BaseModel):
    encodings: List[List[float]]
    names: List[str]

def dowload_file(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        print(bucket_name, datetime.now())
        return True
    except Exception as e:
        print(e)
        return False

def list_file(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    files = []

    for blob in blobs:
        files.append((blob_metadata(bucket_name, blob.name)))

    return files

def blob_metadata(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    return {'file': blob.name, 'bucket': blob.bucket.name, 'updated': blob.updated}
    
def date_file(date):
  return date['updated']

def last_dat_sort(): 
    # print('last date')
    datFiles = list_file(bucket_name_biometria)
    datFiles.sort(key=date_file, reverse=True)
    # print(datFiles[0]['updated'])

    return datFiles

def compare_download_file(file1, file2):
    # print('compare')
    # print(file1)
    global lastDat
    global lastPicke

    if file1 != null and file1['updated'] != file2['updated'] :
        if file2['file'] == 'encodings.pickle':
            dowload_file('encodings.pickle', os.path.join(os.getcwd(), 'encodings.pickle'), bucket_name_pickle)
            lastPicke = file2
        else: 
            dowload_file(file2['file'], os.path.join(os.getcwd(), './biometria/{nome}').format(nome = file2['file']), bucket_name_biometria)
            lastDat = file2
    
        print('importação realizada do arquivo', file2['file'], 'enviado às', file2['updated'])
    else:
        if file2['file'] == 'encodings.pickle':
            lastPicke = file2
            # print('else', lastPicke)
        else:
            lastDat = file2
            # print('else', lastDat)
    
schedule.every(0).minutes.do(lambda: print('Verificando atualizações -', datetime.now()))
schedule.every(0).minutes.do(lambda: compare_download_file(lastPicke, list_file(bucket_name_pickle)[0]))
schedule.every(0).minutes.do(lambda: compare_download_file(lastDat, last_dat_sort()[0]))

while True:
    schedule.run_pending()
    time.sleep(30)