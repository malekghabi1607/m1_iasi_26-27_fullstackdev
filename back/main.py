from fastapi import FastAPI, HTTPException
import uvicorn
from pathlib import Path
from typing import List
from src.models import ArbreGenealogique, Personne, Lien
from src.persistence import MoteurPersistence

app = FastAPI()


@app.get('/')
async def root():
    return 'Hello world, bonjour, konichiwa'


# === Routes pour Personnes ===
@app.get('/personnes', response_model=List[Personne])
async def get_all_personnes():
    """Récupère la liste complète des personnes.
    Retourne:
        List[Personne]: Liste des personnes.
    """
    pass


@app.get('/personnes/{personne_id}', response_model=Personne)
async def get_personne_by_id(personne_id: str):
    """Récupère une personne par son ID.
    Args:
        personne_id (str): ID de la personne.
    Retourne:
        Personne: Objet Personne correspondant.
    Erreurs:
        HTTPException 404: Si la personne n'existe pas.
    """
    pass


@app.post('/personnes', response_model=Personne)
async def create_personne(personne: Personne):
    """Crée une nouvelle personne.
    Args:
        personne (Personne): Objet Personne à créer.
    Retourne:
        Personne: Objet Personne créé.
    Erreurs:
        HTTPException 400: Si l'ID existe déjà.
    """
    pass


@app.put('/personnes/{personne_id}', response_model=Personne)
async def update_personne(personne_id: str, updates: dict):
    """Met à jour une personne existante.
    Args:
        personne_id (str): ID de la personne à mettre à jour.
        updates (dict): Dictionnaire des champs à mettre à jour.
    Retourne:
        Personne: Objet Personne mis à jour.
    Erreurs:
        HTTPException 404: Si la personne n'existe pas.
    """
    pass


@app.delete('/personnes/{personne_id}')
async def delete_personne(personne_id: str):
    """Supprime une personne par son ID.
    Args:
        personne_id (str): ID de la personne à supprimer.
    Retourne:
        None: Confirmation de suppression.
    Erreurs:
        HTTPException 404: Si la personne n'existe pas.
    """
    pass


# === Routes pour Liens ===
@app.get('/liens', response_model=List[Lien])
async def get_all_liens():
    """Récupère la liste complète des liens.
    Retourne:
        List[Lien]: Liste des liens.
    """
    pass


@app.get('/liens/{lien_id}', response_model=Lien)
async def get_lien_by_id(lien_id: str):
    """Récupère un lien par son ID.
    Args:
        lien_id (str): ID du lien.
    Retourne:
        Lien: Objet Lien correspondant.
    Erreurs:
        HTTPException 404: Si le lien n'existe pas.
    """
    pass


@app.post('/liens', response_model=Lien)
async def create_lien(lien: Lien):
    """Crée un nouveau lien.
    Args:
        lien (Lien): Objet Lien à créer.
    Retourne:
        Lien: Objet Lien créé.
    Erreurs:
        HTTPException 400: Si l'ID existe déjà.
    """
    pass


@app.put('/liens/{lien_id}', response_model=Lien)
async def update_lien(lien_id: str, updates: dict):
    """Met à jour un lien existant.
    Args:
        lien_id (str): ID du lien à mettre à jour.
        updates (dict): Dictionnaire des champs à mettre à jour.
    Retourne:
        Lien: Objet Lien mis à jour.
    Erreurs:
        HTTPException 404: Si le lien n'existe pas.
    """
    pass


@app.delete('/liens/{lien_id}')
async def delete_lien(lien_id: str):
    """Supprime un lien par son ID.
    Args:
        lien_id (str): ID du lien à supprimer.
    Retourne:
        None: Confirmation de suppression.
    Erreurs:
        HTTPException 404: Si le lien n'existe pas.
    """
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9999, reload=False)
