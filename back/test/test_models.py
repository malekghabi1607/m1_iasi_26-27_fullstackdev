import pytest
from pydantic import ValidationError

from src.models import (
    ArbreGenealogique,
    Lien,
    LienType,
    Personne,
)


def test_personne_avec_champs_obligatoires():
    personne = Personne(id="42")

    assert personne.id == "42"
    assert personne.nom_famille is None
    assert personne.prenom is None
    assert personne.date_naissance is None
    assert personne.nationalite is None


def test_personne_accepte_tous_les_champs():
    personne = Personne(
        id="42",
        nom_famille="Dupont",
        prenom="Alice",
        lieu_naissance="Paris",
        date_naissance="1990-05-12",
        lieu_mort="Lyon",
        date_mort="2020",
        nationalite="Française",
    )

    assert personne.nom_famille == "Dupont"
    assert personne.prenom == "Alice"
    assert personne.lieu_naissance == "Paris"
    assert personne.date_naissance == "1990-05-12"
    assert personne.lieu_mort == "Lyon"
    assert personne.date_mort == "2020"
    assert personne.nationalite == "Française"


def test_personne_exige_un_id():
    with pytest.raises(ValidationError):
        Personne()


@pytest.mark.parametrize("date", ["1990", "1990-05-12"])
def test_personne_accepte_les_formats_de_date_valides(date):
    personne = Personne(
        id="42",
        date_naissance=date,
        date_mort=date,
    )

    assert personne.date_naissance == date
    assert personne.date_mort == date


@pytest.mark.parametrize("date", ["12/05/1990", "1990-5-12", "abc"])
def test_personne_refuse_un_format_de_date_invalide(date):
    with pytest.raises(ValidationError):
        Personne(id="42", date_naissance=date)


def test_lien_accepte_un_type_parent():
    lien = Lien(
        id="1",
        source="42",
        destination="44",
        type=LienType.PARENT,
    )

    assert lien.id == "1"
    assert lien.source == "42"
    assert lien.destination == "44"
    assert lien.type == LienType.PARENT


def test_lien_accepte_un_type_partenaire():
    lien = Lien(
        id="2",
        source="42",
        destination="44",
        type="partenaire",
    )

    assert lien.type == LienType.PARTENAIRE


def test_lien_refuse_un_type_inconnu():
    with pytest.raises(ValidationError):
        Lien(
            id="1",
            source="42",
            destination="44",
            type="ami",
        )


def test_lien_exige_ses_champs():
    with pytest.raises(ValidationError):
        Lien(
            id="1",
            source="42",
            destination="44",
        )


def test_arbre_genealogique_accepte_personnes_et_liens():
    personne = Personne(id="42", prenom="Alice")
    lien = Lien(
        id="1",
        source="42",
        destination="44",
        type=LienType.PARTENAIRE,
    )

    arbre = ArbreGenealogique(
        personnes=[personne],
        liens=[lien],
    )

    assert len(arbre.personnes) == 1
    assert arbre.personnes[0].prenom == "Alice"
    assert len(arbre.liens) == 1
    assert arbre.liens[0].type == LienType.PARTENAIRE


def test_arbre_genealogique_accepte_des_listes_vides():
    arbre = ArbreGenealogique(personnes=[], liens=[])

    assert arbre.personnes == []
    assert arbre.liens == []


def test_arbre_genealogique_exige_personnes_et_liens():
    with pytest.raises(ValidationError):
        ArbreGenealogique()