"""Shared fixtures for all test files in the back/test directory."""

import pytest

from src.models import ArbreGenealogique, Lien, LienType, Personne


# Fixtures pour Personne
@pytest.fixture
def personne_valide():
    return Personne(
        id="p_001",
        nom_famille="Dupont",
        prenom="Jean",
        lieu_naissance="Paris",
        date_naissance="1990-05-15",
        lieu_mort="Lyon",
        date_mort="2020",
        nationalite="Française"
    )


@pytest.fixture
def personne_minimale():
    return Personne(id="p_002")


@pytest.fixture
def personne_invalide_sans_id():
    return {"nom_famille": "Martin", "prenom": "Pierre"}


@pytest.fixture
def personne_invalide_date():
    return {"id": "p_003", "date_naissance": "15-05-1990"}


# Fixtures pour Lien
@pytest.fixture
def lien_valide():
    return Lien(
        id="l_001",
        source="p_001",
        destination="p_002",
        type=LienType.PARENT
    )


@pytest.fixture
def lien_partenaire():
    return Lien(
        id="l_002",
        source="p_001",
        destination="p_002",
        type=LienType.PARTENAIRE
    )


@pytest.fixture
def lien_invalide_sans_type():
    return {"id": "l_003", "source": "p_001", "destination": "p_002"}


@pytest.fixture
def lien_invalide_type():
    return {"id": "l_004", "source": "p_001", "destination": "p_002", "type": "ami"}


# Fixtures pour ArbreGenealogique
@pytest.fixture
def arbre_valide(personne_valide, personne_minimale, lien_valide):
    return ArbreGenealogique(
        personnes=[personne_valide, personne_minimale],
        liens=[lien_valide]
    )


@pytest.fixture
def arbre_vide():
    return ArbreGenealogique(personnes=[], liens=[])


@pytest.fixture
def arbre_invalide_sans_personnes():
    return {"liens": []}


@pytest.fixture
def arbre_invalide_sans_liens():
    return {"personnes": []}
