import os

from fastapi import FastAPI
import uvicorn
from pathlib import Path
from src.models import ArbreGenealogique, Personne
from src.persistence import MoteurPersistence

app = FastAPI()


@app.get('/')
async def root():
    return 'Hello world, bonjour, konichiwa'


@app.get('/personnes')
async def get_personnes():
    loaded_file: ArbreGenealogique = MoteurPersistence.load('./data/example.json')
    return loaded_file.personnes
    # return 'je suis censé être la liste des personnes'


@app.post('/personne')
async def post_personne():
    """Je suis censé récupérer des data envoyes par le client et les ecrire
    dans le fichier"""
    return ''


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=False)
