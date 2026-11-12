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


@pytest.fixture
def client_liens(fichier_arbre_avec_lien, monkeypatch):
    """Client HTTP de test, branché sur un fichier JSON temporaire qui contient un lien."""
    monkeypatch.setattr(MoteurPersistence, "FICHIER", fichier_arbre_avec_lien)
    return TestClient(app)


class TestGetPersonnes:
    """Tests pour la route GET /personnes."""

    def test_get_personnes_lit_le_fichier_de_donnees(self, client):
        """Vérifie que GET /personnes renvoie les personnes de FICHIER."""
        reponse = client.get("/personnes")

        assert reponse.status_code == 200
        assert [p["id"] for p in reponse.json()] == ["p_001"]


class TestGetPersonne:
    """Tests pour la route GET /personnes/{personne_id}."""

    def test_get_personne_existante(self, client):
        """Vérifie que GET /personnes/{id} renvoie la personne demandée."""
        reponse = client.get("/personnes/p_001")

        assert reponse.status_code == 200
        assert reponse.json()["id"] == "p_001"
        assert reponse.json()["nom_famille"] == "Dupont"

    def test_get_personne_inexistante_renvoie_404(self, client):
        """Vérifie que GET /personnes/{id} renvoie 404 si la personne n'existe pas."""
        reponse = client.get("/personnes/p_999")

        assert reponse.status_code == 404


class TestPostPersonne:
    """Tests pour la route POST /personnes."""

    def test_post_personne_cree_la_personne(self, client):
        """Vérifie que POST /personnes ajoute la personne dans le fichier."""
        reponse = client.post("/personnes", json={"id": "p_002", "prenom": "Marie"})

        assert reponse.status_code == 200
        assert reponse.json()["id"] == "p_002"
        assert client.get("/personnes/p_002").json()["prenom"] == "Marie"

    def test_post_personne_existante_renvoie_400(self, client):
        """Vérifie que POST /personnes renvoie 400 si l'id existe déjà."""
        reponse = client.post("/personnes", json={"id": "p_001"})

        assert reponse.status_code == 400

    def test_post_personne_invalide_renvoie_422(self, client):
        """Vérifie que POST /personnes renvoie 422 si les données sont invalides."""
        reponse = client.post("/personnes", json={"id": "p_003", "date_naissance": "12/05/1990"})

        assert reponse.status_code == 422


class TestPutPersonne:
    """Tests pour la route PUT /personnes/{personne_id}."""

    def test_put_personne_modifie_la_personne(self, client):
        """Vérifie que PUT /personnes/{id} enregistre la modification."""
        reponse = client.put("/personnes/p_001", json={"prenom": "Pierre"})

        assert reponse.status_code == 200
        assert client.get("/personnes/p_001").json()["prenom"] == "Pierre"

    def test_put_personne_inexistante_renvoie_404(self, client):
        """Vérifie que PUT /personnes/{id} renvoie 404 si la personne n'existe pas."""
        reponse = client.put("/personnes/p_999", json={"prenom": "Pierre"})

        assert reponse.status_code == 404

    def test_put_personne_date_invalide_renvoie_422(self, client):
        """Vérifie que PUT /personnes/{id} renvoie 422 si la nouvelle date est invalide."""
        reponse = client.put("/personnes/p_001", json={"date_naissance": "12/05/1990"})

        assert reponse.status_code == 422


class TestDeletePersonne:
    """Tests pour la route DELETE /personnes/{personne_id}."""

    def test_delete_personne_supprime_la_personne(self, client):
        """Vérifie que DELETE /personnes/{id} retire la personne du fichier."""
        reponse = client.delete("/personnes/p_001")

        assert reponse.status_code == 200
        assert client.get("/personnes").json() == []

    def test_delete_personne_inexistante_renvoie_404(self, client):
        """Vérifie que DELETE /personnes/{id} renvoie 404 si la personne n'existe pas."""
        reponse = client.delete("/personnes/p_999")

        assert reponse.status_code == 404


class TestGetLiens:
    """Tests pour les routes GET /liens et GET /liens/{lien_id}."""

    def test_get_liens_lit_le_fichier_de_donnees(self, client_liens):
        """Vérifie que GET /liens renvoie les liens de FICHIER."""
        reponse = client_liens.get("/liens")

        assert reponse.status_code == 200
        assert [l["id"] for l in reponse.json()] == ["l_001"]

    def test_get_lien_existant(self, client_liens):
        """Vérifie que GET /liens/{id} renvoie le lien demandé."""
        reponse = client_liens.get("/liens/l_001")

        assert reponse.status_code == 200
        assert reponse.json()["source"] == "p_001"

    def test_get_lien_inexistant_renvoie_404(self, client_liens):
        """Vérifie que GET /liens/{id} renvoie 404 si le lien n'existe pas."""
        reponse = client_liens.get("/liens/l_999")

        assert reponse.status_code == 404


class TestPostLien:
    """Tests pour la route POST /liens."""

    def test_post_lien_cree_le_lien(self, client_liens):
        """Vérifie que POST /liens ajoute le lien dans le fichier."""
        reponse = client_liens.post(
            "/liens",
            json={"id": "l_002", "source": "p_002", "destination": "p_003", "type": "partenaire"},
        )

        assert reponse.status_code == 200
        assert client_liens.get("/liens/l_002").json()["type"] == "partenaire"

    def test_post_lien_existant_renvoie_400(self, client_liens):
        """Vérifie que POST /liens renvoie 400 si l'id existe déjà."""
        reponse = client_liens.post(
            "/liens",
            json={"id": "l_001", "source": "p_001", "destination": "p_002", "type": "parent"},
        )

        assert reponse.status_code == 400

    def test_post_lien_type_invalide_renvoie_422(self, client_liens):
        """Vérifie que POST /liens renvoie 422 si le type n'existe pas."""
        reponse = client_liens.post(
            "/liens",
            json={"id": "l_003", "source": "p_001", "destination": "p_002", "type": "ami"},
        )

        assert reponse.status_code == 422


class TestReglesApi:
    """Les règles de l'arbre renvoient une erreur 400 avec un message clair."""

    @pytest.mark.parametrize("source,destination", [("p_002", "p_003"), ("p_003", "p_002")])
    def test_second_partenaire_renvoie_400(self, client_liens, source, destination):
        premier = client_liens.post("/liens", json={"id": "l_partenaire", "source": "p_001", "destination": "p_003", "type": "partenaire"})
        assert premier.status_code == 200
        reponse = client_liens.post("/liens", json={"id": "l_second", "source": source, "destination": destination, "type": "partenaire"})
        assert reponse.status_code == 400
        assert "un seul partenaire" in reponse.json()["detail"]
        assert len(client_liens.get("/liens").json()) == 2

    def test_modification_vers_un_second_partenaire_renvoie_400(self, client_liens):
        premier = client_liens.post("/liens", json={"id": "l_partenaire", "source": "p_001", "destination": "p_003", "type": "partenaire"})
        assert premier.status_code == 200
        reponse = client_liens.put("/liens/l_001", json={"source": "p_002", "destination": "p_003", "type": "partenaire"})
        assert reponse.status_code == 400
        assert "un seul partenaire" in reponse.json()["detail"]
        assert client_liens.get("/liens/l_001").json()["type"] == "parent"

    @pytest.mark.parametrize("source,destination", [("p_001", "p_002"), ("p_002", "p_001")])
    def test_partenariat_parent_enfant_renvoie_400(self, client_liens, source, destination):
        reponse = client_liens.post(
            "/liens",
            json={"id": "l_interdit", "source": source, "destination": destination, "type": "partenaire"},
        )
        assert reponse.status_code == 400
        assert "parent et son enfant" in reponse.json()["detail"]
        assert [l["id"] for l in client_liens.get("/liens").json()] == ["l_001"]

    def test_lien_parent_entre_partenaires_renvoie_400(self, client_liens):
        client_liens.post("/liens", json={"id": "l_partenaire", "source": "p_001", "destination": "p_003", "type": "partenaire"})
        reponse = client_liens.post("/liens", json={"id": "l_interdit", "source": "p_001", "destination": "p_003", "type": "parent"})
        assert reponse.status_code == 400
        assert "partenaires" in reponse.json()["detail"]

    def test_modification_partenariat_vers_enfant_renvoie_400(self, client_liens):
        client_liens.post("/liens", json={"id": "l_partenaire", "source": "p_001", "destination": "p_003", "type": "partenaire"})
        reponse = client_liens.put("/liens/l_partenaire", json={"destination": "p_002"})
        assert reponse.status_code == 400
        assert "parent et son enfant" in reponse.json()["detail"]
        assert client_liens.get("/liens/l_partenaire").json()["destination"] == "p_003"

    def test_post_lien_vers_soi_meme_renvoie_400(self, client_liens):
        reponse = client_liens.post(
            "/liens",
            json={"id": "l_009", "source": "p_001", "destination": "p_001", "type": "partenaire"},
        )

        assert reponse.status_code == 400
        assert "elle-même" in reponse.json()["detail"]

    def test_put_lien_vers_soi_meme_renvoie_400(self, client_liens):
        reponse = client_liens.put("/liens/l_001", json={"destination": "p_001"})

        assert reponse.status_code == 400


class TestPutLien:
    """Tests pour la route PUT /liens/{lien_id}."""

    def test_put_lien_modifie_le_lien(self, client_liens):
        """Vérifie que PUT /liens/{id} enregistre la modification."""
        reponse = client_liens.put("/liens/l_001", json={"type": "partenaire"})

        assert reponse.status_code == 200
        assert client_liens.get("/liens/l_001").json()["type"] == "partenaire"

    def test_put_lien_inexistant_renvoie_404(self, client_liens):
        """Vérifie que PUT /liens/{id} renvoie 404 si le lien n'existe pas."""
        reponse = client_liens.put("/liens/l_999", json={"type": "partenaire"})

        assert reponse.status_code == 404

    def test_put_lien_type_invalide_renvoie_422(self, client_liens):
        """Vérifie que PUT /liens/{id} renvoie 422 si le nouveau type est invalide."""
        reponse = client_liens.put("/liens/l_001", json={"type": "ami"})

        assert reponse.status_code == 422


class TestDeleteLien:
    """Tests pour la route DELETE /liens/{lien_id}."""

    def test_delete_lien_supprime_le_lien(self, client_liens):
        """Vérifie que DELETE /liens/{id} retire le lien du fichier."""
        reponse = client_liens.delete("/liens/l_001")

        assert reponse.status_code == 200
        assert client_liens.get("/liens").json() == []

    def test_delete_lien_inexistant_renvoie_404(self, client_liens):
        """Vérifie que DELETE /liens/{id} renvoie 404 si le lien n'existe pas."""
        reponse = client_liens.delete("/liens/l_999")

        assert reponse.status_code == 404


class TestCors:
    """Tests pour l'autorisation CORS (appels depuis le front)."""

    def test_api_autorise_les_appels_du_front(self, client):
        """Vérifie que l'API autorise un navigateur à l'appeler depuis une autre origine."""
        reponse = client.get("/personnes", headers={"Origin": "http://localhost:5500"})

        assert reponse.headers.get("access-control-allow-origin") == "*"
