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
