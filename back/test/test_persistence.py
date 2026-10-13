import json
from pathlib import Path
import pytest
from src.models import Personne, ArbreGenealogique
from persistence import MoteurPersistence


@pytest.fixture
def moi():
    return Personne(
        id="222",
        nom_famille="Rousseau",
        prenom="Rayane",
        lieu_naissance="Dunkerque",
        date_naissance="1972-09-25",
        nationalite="Français",
    )
    
@pytest.fixture
def chemin():
    return Path("test_data/data.json")


@pytest.fixture
def arbre(moi):
    return ArbreGenealogique(personnes=[moi], liens=[])


def test_dump_cree_le_fichier(arbre, moi, chemin):
    
    MoteurPersistence.dump(arbre, str(chemin))

    assert chemin.exists()
    data = json.loads(chemin.read_text(encoding="utf-8"))
    assert moi.model_dump() in data["personnes"]
