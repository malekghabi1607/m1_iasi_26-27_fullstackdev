from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from src.models import ArbreGenealogique, Personne
from src.persistence import MoteurPersistence

app = FastAPI()

# autorise le front (page HTML ouverte dans le navigateur) à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return 'Hello world, bonjour, konichiwa'


@app.get('/personnes')
async def get_personnes():
    loaded_file: ArbreGenealogique = MoteurPersistence.load(MoteurPersistence.FICHIER)
    return loaded_file.personnes
    # return 'je suis censé être la liste des personnes'


@app.get('/personne/{personne_id}')
async def get_personne(personne_id: str):
    try:
        return MoteurPersistence.get_personne(MoteurPersistence.FICHIER, personne_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post('/personne', status_code=201)
async def post_personne(personne: Personne):
    """Récupère la personne envoyée par le client et l'écrit dans le fichier."""
    try:
        MoteurPersistence.create_personne(MoteurPersistence.FICHIER, personne)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return personne


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=False)
