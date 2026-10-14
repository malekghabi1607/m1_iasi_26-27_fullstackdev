"""
Tests pour les opérations CRUD sur les personnes.

Objectif : Tester les opérations unitaires sur les personnes (création, lecture, mise à jour, suppression).
"""

import pytest
from pydantic import ValidationError

from src.models import Personne


class TestCreatePersonne:
    """Tests pour la création d'une personne."""

    def test_creer_personne_avec_id_uniquement(self):
        """
        TODO: Vérifier qu'une personne peut être créée avec uniquement un ID.
        Indice : Utiliser Personne(id="123").
        """
        personne = Personne(id="123")

        assert personne.id == "123"
        assert personne.nom_famille is None
        assert personne.prenom is None

    def test_creer_personne_avec_tous_les_champs(self):
        """
        TODO: Vérifier qu'une personne peut être créée avec tous les champs valides.
        Indice : Utiliser Personne(id="123", nom_famille="Dupont", prenom="Jean", ...).
        """
        personne = Personne(
            id="123",
            nom_famille="Dupont",
            prenom="Jean",
            lieu_naissance="Lille",
            date_naissance="2000-05-15",
            lieu_mort="Lille",
            date_mort="2020",
            nationalite="Française",
        )

        assert personne.nom_famille == "Dupont"
        assert personne.prenom == "Jean"
        assert personne.date_naissance == "2000-05-15"
        assert personne.date_mort == "2020"


    def test_creer_personne_sans_id_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est manquant.
        Indice : Utiliser pytest.raises(ValidationError) et Personne().
        """
        with pytest.raises(ValidationError):
            Personne()


    def test_creer_personne_avec_id_invalide_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide).
        Indice : Tester avec Personne(id=None) et Personne(id="").
        """
        with pytest.raises(ValidationError):
            Personne(id=None)
        with pytest.raises(ValidationError):
            Personne(id="")



class TestReadPersonne:
    """Tests pour la lecture des informations d'une personne."""

    def test_lire_personne_avec_id_valide_et_ressource_presente(self, arbre_valide):
        """
        TODO: Vérifier qu'une personne peut être lue avec un ID valide et que la ressource existe.
        Indice : Créer une Personne(id="123") et vérifier que personne.id == "123".
        """
        personnes = {p.id: p for p in arbre_valide.personnes}

        assert personnes["p_001"].prenom == "Jean"


    def test_lire_personne_avec_id_valide_et_ressource_manquante(self, arbre_valide):
        """
        TODO: Vérifier qu'une erreur est levée si l'ID est valide mais que la ressource n'existe pas.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: KeyError ou ValueError).
        """
        personnes = {p.id: p for p in arbre_valide.personnes}

        with pytest.raises(KeyError):
            personnes["p_999"]


    def test_lire_personne_avec_id_invalide(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide).
        Indice : Utiliser pytest.raises(ValidationError) et Personne(id=None) ou Personne(id="").
        """
        with pytest.raises(ValidationError):
            Personne(id=None)
        with pytest.raises(ValidationError):
            Personne(id="")



class TestUpdatePersonne:
    """Tests pour la mise à jour des informations d'une personne."""

    def test_mettre_a_jour_nom_famille(self):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec un nouveau nom de famille.
        Indice : Créer une Personne, puis modifier son nom_famille et vérifier la mise à jour.
        """
        pass

    def test_mettre_a_jour_prenom(self):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec un nouveau prénom.
        Indice : Créer une Personne, puis modifier son prenom et vérifier la mise à jour.
        """
        pass

    def test_mettre_a_jour_date_naissance(self):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec une nouvelle date de naissance.
        Indice : Créer une Personne, puis modifier sa date_naissance et vérifier la mise à jour.
        """
        pass

    def test_mettre_a_jour_avec_date_invalide_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si une date invalide est assignée.
        Indice : Utiliser pytest.raises(ValidationError) et assigner une date comme "12/05/1990".
        """
        pass


class TestDeletePersonne:
    """Tests pour la suppression d'une personne."""

    def test_supprimer_personne(self):
        """
        TODO: Vérifier qu'une personne peut être supprimée (ex: en utilisant del ou une méthode dédiée).
        Indice : Si une liste de personnes est utilisée, vérifier que la personne est retirée.
        """
        pass

    def test_supprimer_personne_inexistante_echoue(self):
        """
        TODO: Vérifier qu'une erreur est levée si on tente de supprimer une personne inexistante.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: ValueError).
        """
        pass
