from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def root():
    return 'Hello world, bonjour, konichiwa'


@app.get('/personnes')
async def get_users():
    return 'je suis censé être la liste des utilisateurs'


@app.post('/user')
async def post_user():
    """Je suis censé récupérer des data envoyes par le client et les ecrire
    dans le fichier"""
    return ''


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=False)
