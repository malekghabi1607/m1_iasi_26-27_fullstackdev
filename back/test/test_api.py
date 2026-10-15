"""
Tests pour les routes HTTP de l'API (main.py).

Objectif : Vérifier que les routes appellent le moteur de persistence
sur le bon fichier de données.
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from src.persistence import MoteurPersistence


@pytest.fixture
def client(fichier_arbre_valide, monkeypatch):
    """Client HTTP de test, branché sur un fichier JSON temporaire."""
    monkeypatch.setattr(MoteurPersistence, "FICHIER", fichier_arbre_valide)
    return TestClient(app)


class TestGetPersonnes:
    """Tests pour la route GET /personnes."""

    def test_get_personnes_lit_le_fichier_de_donnees(self, client):
        """Vérifie que GET /personnes renvoie les personnes de FICHIER."""
        reponse = client.get("/personnes")

        assert reponse.status_code == 200
        assert [p["id"] for p in reponse.json()] == ["p_001"]


class TestGetPersonne:
    """Tests pour la route GET /personne/{personne_id}."""

    def test_get_personne_existante(self, client):
        """Vérifie que GET /personne/{id} renvoie la personne demandée."""
        reponse = client.get("/personne/p_001")

        assert reponse.status_code == 200
        assert reponse.json()["id"] == "p_001"
        assert reponse.json()["nom_famille"] == "Dupont"

    def test_get_personne_inexistante_renvoie_404(self, client):
        """Vérifie que GET /personne/{id} renvoie 404 si la personne n'existe pas."""
        reponse = client.get("/personne/p_999")

        assert reponse.status_code == 404


class TestPostPersonne:
    """Tests pour la route POST /personne."""

    def test_post_personne_cree_la_personne(self, client):
        """Vérifie que POST /personne ajoute la personne dans le fichier."""
        reponse = client.post("/personne", json={"id": "p_002", "prenom": "Marie"})

        assert reponse.status_code == 201
        assert reponse.json()["id"] == "p_002"
        assert client.get("/personne/p_002").json()["prenom"] == "Marie"

    def test_post_personne_existante_renvoie_409(self, client):
        """Vérifie que POST /personne renvoie 409 si l'id existe déjà."""
        reponse = client.post("/personne", json={"id": "p_001"})

        assert reponse.status_code == 409

    def test_post_personne_invalide_renvoie_422(self, client):
        """Vérifie que POST /personne renvoie 422 si les données sont invalides."""
        reponse = client.post("/personne", json={"id": "p_003", "date_naissance": "12/05/1990"})

        assert reponse.status_code == 422


class TestCors:
    """Tests pour l'autorisation CORS (appels depuis le front)."""

    def test_api_autorise_les_appels_du_front(self, client):
        """Vérifie que l'API autorise un navigateur à l'appeler depuis une autre origine."""
        reponse = client.get("/personnes", headers={"Origin": "http://localhost:5500"})

        assert reponse.headers.get("access-control-allow-origin") == "*"
