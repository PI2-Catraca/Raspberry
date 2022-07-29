from fastapi import FastAPI
import pickle
from pydantic import BaseModel

class Pickle(BaseModel):
    imagem: str

app = FastAPI()

@app.post("/api/encondings")
async def teste(data: Pickle):
    f = open("encodings.pickle", "wb")
    f.write(data['imagem'])