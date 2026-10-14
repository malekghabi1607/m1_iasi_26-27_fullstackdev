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

    def test_creer_personne_avec_id_uniquement(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être créée avec uniquement un ID via le moteur de persistence.
        """
        nouvelle_personne = Personne(id="p_002")
        MoteurPersistence.create_personne(fichier_arbre_valide, nouvelle_personne)

        arbre_charge = MoteurPersistence.load(fichier_arbre_valide)
        assert len(arbre_charge.personnes) == 2
        assert any(p.id == "p_002" for p in arbre_charge.personnes)

    def test_creer_personne_avec_tous_les_champs(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être créée avec tous les champs valides via le moteur de persistence.
        """
        nouvelle_personne = Personne(
            id="p_002",
            nom_famille="Martin",
            prenom="Marie",
            lieu_naissance="Marseille",
            date_naissance="1995-08-20",
            nationalite="Française"
        )
        MoteurPersistence.create_personne(fichier_arbre_valide, nouvelle_personne)
        
        arbre_charge = MoteurPersistence.load(fichier_arbre_valide)
        assert len(arbre_charge.personnes) == 2
        personne_trouvee = next(p for p in arbre_charge.personnes if p.id == "p_002")
        assert personne_trouvee.nom_famille == "Martin"
        assert personne_trouvee.prenom == "Marie"

    def test_creer_personne_leve_erreur_si_personne_existante(self, fichier_arbre_valide):
        nouvelle_personne = Personne(id='p_001')

        with pytest.raises(ValueError):
            MoteurPersistence.create_personne(fichier_arbre_valide, nouvelle_personne)

    def test_test_creer_personne_leve_erreur_si_appel_avec_non_personne(self, fichier_arbre_valide):
        nouvelle_personne = {
            'id': "p_001",
            'nom_famille': "Dupont",
            'prenom': "Jean",
            'lieu_naissance': "Paris",
            'date_naissance': "1990-05-15"
        }

        with pytest.raises(ValueError):
            MoteurPersistence.create_personne(fichier_arbre_valide, nouvelle_personne)

class TestReadPersonne:
    """Tests pour la lecture des informations d'une personne."""

    def test_lire_personne_avec_id_valide_et_ressource_presente(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être lue avec un ID valide et que la ressource existe.
        """
        personne = MoteurPersistence.get_personne(fichier_arbre_valide, "p_001")
        assert personne.id == "p_001"
        assert personne.nom_famille == "Dupont"

    def test_lire_personne_avec_id_valide_et_ressource_manquante(self, fichier_arbre_valide):
        """
        Vérifier qu'une erreur est levée si l'ID est valide mais que la ressource n'existe pas.
        """
        with pytest.raises(ValueError):
            MoteurPersistence.get_personne(fichier_arbre_valide, "p_999")

    def test_lire_personne_avec_id_invalide(self, fichier_arbre_valide):
        """
        Vérifier qu'une erreur est levée si l'ID est invalide.
        """
        with pytest.raises(ValueError):
            MoteurPersistence.get_personne(fichier_arbre_valide, None)


class TestUpdatePersonne:
    """Tests pour la mise à jour des informations d'une personne."""

    def test_mettre_a_jour_nom_famille(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être mise à jour avec un nouveau nom de famille.
        """
        MoteurPersistence.update_personne(fichier_arbre_valide, "p_001", {'nom_famille': "Martin"})
        personne = MoteurPersistence.get_personne(fichier_arbre_valide, "p_001")
        assert personne.nom_famille == "Martin"

    def test_mettre_a_jour_prenom(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être mise à jour avec un nouveau prénom.
        """
        MoteurPersistence.update_personne(fichier_arbre_valide, "p_001", {'prenom': "Pierre"})
        personne = MoteurPersistence.get_personne(fichier_arbre_valide, "p_001")
        assert personne.prenom == "Pierre"

    def test_mettre_a_jour_date_naissance(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être mise à jour avec une nouvelle date de naissance.
        """
        MoteurPersistence.update_personne(fichier_arbre_valide, "p_001", {'date_naissance': "1980-01-01"})
        personne = MoteurPersistence.get_personne(fichier_arbre_valide, "p_001")
        assert personne.date_naissance == "1980-01-01"

    def test_mettre_a_jour_avec_date_invalide_echoue(self, fichier_arbre_valide):
        """
        Vérifier qu'une ValidationError est levée si une date invalide est assignée.
        """
        with pytest.raises(ValidationError):
            MoteurPersistence.update_personne(fichier_arbre_valide, "p_001", {'date_naissance': "12/05/1990"})


class TestDeletePersonne:
    """Tests pour la suppression d'une personne."""

    def test_supprimer_personne(self, fichier_arbre_valide):
        """
        Vérifier qu'une personne peut être supprimée.
        """
        MoteurPersistence.delete_personne(fichier_arbre_valide, "p_001")
        arbre_charge = MoteurPersistence.load(fichier_arbre_valide)
        assert len(arbre_charge.personnes) == 0

    def test_supprimer_personne_inexistante_echoue(self, fichier_arbre_valide):
        """
        Vérifier qu'aucune erreur n'est levée si on tente de supprimer une personne inexistante.
        """
        MoteurPersistence.delete_personne(fichier_arbre_valide, "p_999")
        arbre_charge = MoteurPersistence.load(fichier_arbre_valide)
        assert len(arbre_charge.personnes) == 1
