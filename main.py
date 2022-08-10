from typing import List
from fastapi import FastAPI
import pickle
from pydantic import BaseModel

class Pickle(BaseModel):
    encodings: List[List[float]]
    names: List[str]

app = FastAPI()
@app.post("/api/encondings")
async def teste(imagem: Pickle):
    objImagem = {
        "encodings": imagem.encodings,
        "names": imagem.names
    }

    with open("encodings.pickle", "wb") as p:
        pickle.dump(objImagem, p)

    return 'arquivo pickle atualizado'