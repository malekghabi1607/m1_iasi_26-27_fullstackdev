from fastapi import FastAPI
import uvicorn
from persistence import PersistenceEngine

app = FastAPI()


@app.get('/')
async def root():
    return 'Hello world, bonjour, konichiwa'


@app.get('/personnes')
async def get_personnes():
    data = PersistenceEngine.read('./data/data.json')
    return data['personnes']


@app.post('/personne')
async def post_personne():
    """Je suis censé récupérer des data envoyes par le client et les ecrire
    dans le fichier"""
    return ''


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=False)
