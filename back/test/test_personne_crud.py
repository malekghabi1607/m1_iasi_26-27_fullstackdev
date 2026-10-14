"""
Tests pour les opérations CRUD sur les personnes.

Objectif : Tester les opérations unitaires sur les personnes (création, lecture, mise à jour, suppression).
"""

import pytest
from pydantic import ValidationError

from src.models import Personne
from src.persistence import MoteurPersistence


class TestCreatePersonne:
    """Tests pour la création d'une personne."""

    def test_creer_personne_avec_id_uniquement(self):
        """
        TODO: Vérifier qu'une personne peut être créée avec uniquement un ID.
        Indice : Utiliser Personne(id="123").
        """
        pass

    def test_creer_personne_avec_tous_les_champs(self):
        """
        TODO: Vérifier qu'une personne peut être créée avec tous les champs valides.
        Indice : Utiliser Personne(id="123", nom_famille="Dupont", prenom="Jean", ...).
        """
        pass

    def test_creer_personne_sans_id_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est manquant.
        Indice : Utiliser pytest.raises(ValidationError) et Personne().
        """
        pass

    def test_creer_personne_avec_id_invalide_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide).
        Indice : Tester avec Personne(id=None) et Personne(id="").
        """
        pass


class TestReadPersonne:
    """Tests pour la lecture des informations d'une personne."""

    def test_lire_personne_avec_id_valide_et_ressource_presente(self):
        """
        TODO: Vérifier qu'une personne peut être lue avec un ID valide et que la ressource existe.
        Indice : Créer une Personne(id="123") et vérifier que personne.id == "123".
        """
        pass

    def test_lire_personne_avec_id_valide_et_ressource_manquante(self):
        """
        TODO: Vérifier qu'une erreur est levée si l'ID est valide mais que la ressource n'existe pas.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: KeyError ou ValueError).
        """
        pass

    def test_lire_personne_avec_id_invalide(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide).
        Indice : Utiliser pytest.raises(ValidationError) et Personne(id=None) ou Personne(id="").
        """
        pass


class TestUpdatePersonne:
    """Tests pour la mise à jour des informations d'une personne."""

    def test_mettre_a_jour_nom_famille(self, fichier_arbre, personne_valide):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec un nouveau nom de famille.
        Indice : Créer une Personne, puis modifier son nom_famille et vérifier la mise à jour.
        """
        nom = "Rousseau"
        update_nom_famille(fichier_arbre, personne_valide, nom)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.nom_famille == nom

    def test_mettre_a_jour_prenom(self, fichier_arbre, personne_valide):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec un nouveau prénom.
        Indice : Créer une Personne, puis modifier son prenom et vérifier la mise à jour.
        """
        prenom = "Rayane"
        update_prenom(fichier_arbre, personne_valide, prenom)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.prenom == prenom

    def test_mettre_a_jour_date_naissance(self, fichier_arbre, personne_valide):
        """
        TODO: Vérifier qu'une personne peut être mise à jour avec une nouvelle date de naissance.
        Indice : Créer une Personne, puis modifier sa date_naissance et vérifier la mise à jour.
        """
        date_naissance = "1999-09-01"
        update_date_naissance(fichier_arbre, personne_valide, date_naissance)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.date_naissance == date_naissance

    def test_mettre_a_jour_avec_date_invalide_echoue(self, fichier_arbre, personne_valide):
        """
        TODO: Vérifier qu'une ValidationError est levée si une date invalide est assignée.
        Indice : Utiliser pytest.raises(ValidationError) et assigner une date comme "12/05/1990".
        """
        date_invalide = "001-92-8"
        with pytest.raises(ValidationError):
            update_date_naissance(fichier_arbre, personne_valide, date_invalide)
        



class TestDeletePersonne:
    """Tests pour la suppression d'une personne."""

    def test_supprimer_personne(self, fichier_arbre, personne_valide):
        """
        TODO: Vérifier qu'une personne peut être supprimée (ex: en utilisant del ou une méthode dédiée).
        Indice : Si une liste de personnes est utilisée, vérifier que la personne est retirée.
        """
        delete_personne(fichier_arbre, personne_valide)
        apres = MoteurPersistence.load(fichier_arbre)
        ids = [personne.id for personne in apres.personnes]
        assert personne_valide.id not in ids

    def test_supprimer_personne_inexistante_echoue(self, fichier_arbre):
        """
        TODO: Vérifier qu'une erreur est levée si on tente de supprimer une personne inexistante.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: ValueError).
        """
        inexistant = Personne(id="p_999")
        with pytest.raises(ValueError):
            delete_personne(fichier_arbre, inexistant)
