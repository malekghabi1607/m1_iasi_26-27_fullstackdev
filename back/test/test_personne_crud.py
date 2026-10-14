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

    def test_creer_personne_avec_id_uniquement(self,personne_minimale):
        """Vérifie qu'une personne créée avec uniquement un id porte bien son id et le reste en None"""
        p = personne_minimale
        assert p.id == "p_002"
        assert p.nom_famille is None
        assert p.prenom is None  
        assert p.lieu_naissance is None
        assert p.date_naissance is None
        assert p.lieu_mort is None
        assert p.date_mort is None    

    def test_creer_personne_avec_tous_les_champs(self, personne_valide):        
        """Vérifie qu'une personne créée avec tous les champs portent bien leurs atributs"""
        p = personne_valide
        assert p.id == "p_001"
        assert p.nom_famille == "Dupont"
        assert p.prenom == "Jean"
        assert p.lieu_naissance == "Paris"
        assert p.date_naissance == "1990-05-15"
        assert p.lieu_mort == "Lyon"
        assert p.date_mort == "2020"
        assert p.nationalite == "Française"

    def test_creer_personne_sans_id_echoue(self, personne_invalide_sans_id):
        """Vérifie qu'une ValidationError est bien levée lors de la création d'une personne sans id"""
        p = personne_invalide_sans_id
        with pytest.raises(ValidationError):
            Personne(**p)

    def test_creer_personne_avec_id_invalide_echoue(self):
        """Vérifie qu'une ValidationError est bien levée lors de la création d'une personne avec un id invalide (None ou \"\")"""
        with pytest.raises(ValidationError):
            Personne(id=None)

        with pytest.raises(ValidationError):
            Personne(id="")


class TestReadPersonne:
    """Tests pour la lecture des informations d'une personne."""

    def test_lire_personne_avec_id_valide_et_ressource_presente(self, personne_minimale):
        """Vérifie qu'un personne valide peut être lue par ses atributs"""
        p = personne_minimale
        assert p.id == "p_002"

    def test_lire_personne_avec_id_valide_et_ressource_manquante(self):
        """Vérifie que la lecture d'une personne avec un id valide mais inexistante lève une KeyError ou une ValueError"""
        personnes = {"01" : Personne(id='01'), "03" : Personne(id='03')}
        with pytest.raises((KeyError,ValueError)):
            print(personnes["02"])

    def test_lire_personne_avec_id_invalide(self):
        """Vérifie que la lecture d'une personne avec un id invalide lève une ValidationError"""
        with pytest.raises(ValidationError):
            print(Personne(id=""))


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
