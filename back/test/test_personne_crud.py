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

    def test_creer_personne_avec_id_uniquement(self,personne_minimale,fichier_arbre):
        """Vérifie qu'une personne créée avec uniquement un id porte bien son id et le reste en None"""
        p = personne_minimale
        MoteurPersistence.create_personne(p,fichier_arbre)
        arbre = MoteurPersistence.load(fichier_arbre)
        assert any(personne.id == "p_002" for personne in arbre.personnes)



    def test_creer_personne_avec_tous_les_champs(self, personne_valide, fichier_arbre):
        """Vérifie qu'une personne complète est correctement enregistrée."""

        p = personne_valide
        MoteurPersistence.create_personne(p, fichier_arbre)
        arbre = MoteurPersistence.load(fichier_arbre)

        personne = next((p for p in arbre.personnes if p.id == "p_001"),None)

        assert personne is not None
        assert personne.id == "p_001"
        assert personne.nom_famille == "Dupont"
        assert personne.prenom == "Jean"
        assert personne.lieu_naissance == "Paris"
        assert personne.date_naissance == "1990-05-15"
        assert personne.lieu_mort == "Lyon"
        assert personne.date_mort == "2020"
        assert personne.nationalite == "Française"

    def test_creer_personne_sans_id_echoue(self, personne_invalide_sans_id,fichier_arbre):
        """Vérifie qu'une ValidationError est bien levée lors de la création d'une personne sans id"""
        p = personne_invalide_sans_id
        with pytest.raises(ValidationError):
            MoteurPersistence.create_personne(p, fichier_arbre)


    def test_creer_personne_avec_id_invalide_echoue(self,fichier_arbre):
        """Vérifie qu'une ValidationError est bien levée lors de la création d'une personne avec un id invalide (None ou "")"""
    
        with pytest.raises(ValidationError):
            p = Personne(id=None)
            MoteurPersistence.create_personne(p, fichier_arbre)

        with pytest.raises(ValidationError):
            p = Personne(id="")
            MoteurPersistence.create_personne(p, fichier_arbre)


class TestReadPersonne:
    """Tests pour la lecture des informations d'une personne."""

    def test_lire_personne_avec_id_valide_et_ressource_presente(self, personne_minimale,fichier_arbre):
        """Vérifie qu'un personne valide peut être lue par ses atributs"""
        MoteurPersistence.create_personne(personne_minimale, fichier_arbre)
        p = MoteurPersistence.get_personne(personne_minimale.id,fichier_arbre)

        assert p is not None
        assert p.id == "p_002"

    def test_lire_personne_avec_id_valide_et_ressource_manquante(self,fichier_arbre):
        """Vérifie que la lecture d'une personne avec un id valide mais inexistante lève une KeyError ou une ValueError"""
        with pytest.raises((KeyError,ValueError)):
            MoteurPersistence.get_personne("p_inexistant",fichier_arbre)

    def test_lire_personne_avec_id_invalide(self,fichier_arbre):
        """Vérifie que la lecture d'une personne avec un id invalide lève une ValidationError"""
        with pytest.raises(ValidationError):
            MoteurPersistence.get_personne("",fichier_arbre)


class TestUpdatePersonne:
    """Tests pour la mise à jour des informations d'une personne."""

    def test_mettre_a_jour_nom_famille(self, fichier_arbre, personne_valide):
        """Vérifie qu'une personne peut être mise à jour avec un nouveau nom de famille."""
        nom = "Rousseau"
        update_nom_famille(fichier_arbre, personne_valide, nom)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.nom_famille == nom

    def test_mettre_a_jour_prenom(self, fichier_arbre, personne_valide):
        """Vérifie qu'une personne peut être mise à jour avec un nouveau prénom."""
        prenom = "Rayane"
        update_prenom(fichier_arbre, personne_valide, prenom)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.prenom == prenom

    def test_mettre_a_jour_date_naissance(self, fichier_arbre, personne_valide):
        """Vérifie qu'une personne peut être mise à jour avec une nouvelle date de naissance."""
        date_naissance = "1999-09-01"
        update_date_naissance(fichier_arbre, personne_valide, date_naissance)
        apres = MoteurPersistence.load(fichier_arbre)
        for personne in apres.personnes:
            if personne.id == personne_valide.id:
                assert personne.date_naissance == date_naissance

    def test_mettre_a_jour_avec_date_invalide_echoue(self, fichier_arbre, personne_valide):
        """Vérifie qu'une ValidationError est levée si une date invalide est assignée."""
        date_invalide = "001-92-8"
        with pytest.raises(ValidationError):
            update_date_naissance(fichier_arbre, personne_valide, date_invalide)
        



class TestDeletePersonne:
    """Tests pour la suppression d'une personne."""

    def test_supprimer_personne(self, fichier_arbre, personne_valide):
        """Vérifie qu'une personne peut être supprimée."""
        delete_personne(fichier_arbre, personne_valide)
        apres = MoteurPersistence.load(fichier_arbre)
        ids = [personne.id for personne in apres.personnes]
        assert personne_valide.id not in ids

    def test_supprimer_personne_inexistante_echoue(self, fichier_arbre):
        """Vérifie qu'une erreur est levée si on tente de supprimer une personne inexistante."""
        inexistant = Personne(id="p_999")
        with pytest.raises(ValueError):
            delete_personne(fichier_arbre, inexistant)
