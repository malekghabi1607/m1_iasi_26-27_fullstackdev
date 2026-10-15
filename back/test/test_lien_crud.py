"""
Tests pour les opérations CRUD sur les liens.

Objectif : Tester les opérations unitaires sur les liens (création, lecture, mise à jour, suppression).
"""

import pytest
from pydantic import ValidationError

from src.models import Lien, LienType
from src.persistence import MoteurPersistence


class TestCreateLien:
    """Tests pour la création d'un lien."""

    def test_creer_lien_avec_champs_obligatoires(self, fichier_arbre_avec_lien):

        """
        TODO: Vérifier qu'un lien peut être créé avec les champs obligatoires (id, source, destination, type).
        Indice : Utiliser Lien(id="1", source="p1", destination="p2", type=LienType.PARENT).
        """
        nouveau_lien = Lien(id="l_002", source="p_002", destination="p_001", type=LienType.PARTENAIRE)
        MoteurPersistence.create_lien(fichier_arbre_avec_lien, nouveau_lien)

        arbre_charge = MoteurPersistence.load(fichier_arbre_avec_lien)
        assert len(arbre_charge.liens) == 2
        assert any(l.id == "l_002" for l in arbre_charge.liens)



    def test_creer_lien_sans_id_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est manquant.
        Indice : Utiliser pytest.raises(ValidationError) et Lien(source="p1", destination="p2", type=LienType.PARENT).
        """
        with pytest.raises(ValidationError):
            Lien(source="p1", destination="p2", type=LienType.PARENT)


    def test_creer_lien_sans_source_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si la source est manquante.
        Indice : Utiliser pytest.raises(ValidationError) et Lien(id="1", destination="p2", type=LienType.PARENT).
        """
        with pytest.raises(ValidationError):
            Lien(id="1", destination="p2", type=LienType.PARENT)


    def test_creer_lien_sans_destination_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si la destination est manquante.
        Indice : Utiliser pytest.raises(ValidationError) et Lien(id="1", source="p1", type=LienType.PARENT).
        """
        with pytest.raises(ValidationError):
            Lien(id="1", source="p1", type=LienType.PARENT)


    def test_creer_lien_sans_type_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si le type est manquant.
        Indice : Utiliser pytest.raises(ValidationError) et Lien(id="1", source="p1", destination="p2").
        """
        with pytest.raises(ValidationError):
            Lien(id="1", source="p1", destination="p2")


    def test_creer_lien_avec_type_invalide_echoue(self):
        """
        TODO: Vérifier qu'une ValidationError est levée si le type est invalide (ex: "ami").
        Indice : Utiliser pytest.raises(ValidationError) et Lien(id="1", source="p1", destination="p2", type="ami").
        """
        with pytest.raises(ValidationError):
            Lien(id="1", source="p1", destination="p2", type="ami")



class TestReadLien:
    """Tests pour la lecture des informations d'un lien."""

    def test_lire_lien_avec_id_valide_et_ressource_presente(self, fichier_arbre_avec_lien):

        """
        TODO: Vérifier qu'un lien peut être lu avec un ID valide et que la ressource existe.
        Indice : Créer un Lien(id="1", ...) et vérifier que lien.id == "1".
        """
        lien = MoteurPersistence.get_lien(fichier_arbre_avec_lien, "l_001")
        assert lien.id == "l_001"
        assert lien.source == "p_001"


    def test_lire_lien_avec_id_valide_et_ressource_manquante(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'une erreur est levée si l'ID est valide mais que la ressource n'existe pas.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: KeyError ou ValueError).
        """
        with pytest.raises(ValueError):
            MoteurPersistence.get_lien(fichier_arbre_avec_lien, "l_999")

    def test_lire_lien_avec_id_invalide(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide).
        Indice : Utiliser pytest.raises(ValidationError) et Lien(id=None, ...).
        """
        with pytest.raises(ValueError):
            MoteurPersistence.get_lien(fichier_arbre_avec_lien, None)


class TestUpdateLien:
    """Tests pour la mise à jour des informations d'un lien."""

    def test_mettre_a_jour_type_lien(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'un lien peut être mis à jour avec un nouveau type valide.
        Indice : Créer un Lien, puis modifier son type et vérifier la mise à jour.
        """
        MoteurPersistence.update_lien(fichier_arbre_avec_lien, "l_001", {"type": LienType.PARTENAIRE})
        lien = MoteurPersistence.get_lien(fichier_arbre_avec_lien, "l_001")
        assert lien.type == LienType.PARTENAIRE

    def test_mettre_a_jour_source_lien(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'un lien peut être mis à jour avec une nouvelle source.
        Indice : Créer un Lien, puis modifier sa source et vérifier la mise à jour.
        """
        MoteurPersistence.update_lien(fichier_arbre_avec_lien, "l_001", {"source": "p_003"})
        lien = MoteurPersistence.get_lien(fichier_arbre_avec_lien, "l_001")
        assert lien.source == "p_003"

    def test_mettre_a_jour_destination_lien(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'un lien peut être mis à jour avec une nouvelle destination.
        Indice : Créer un Lien, puis modifier sa destination et vérifier la mise à jour.
        """
        MoteurPersistence.update_lien(fichier_arbre_avec_lien, "l_001", {"destination": "p_003"})
        lien = MoteurPersistence.get_lien(fichier_arbre_avec_lien, "l_001")
        assert lien.destination == "p_003"

    def test_mettre_a_jour_avec_type_invalide_echoue(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'une ValidationError est levée si un type invalide est assigné.
        Indice : Utiliser pytest.raises(ValidationError) et assigner un type comme "ami".
        """
        with pytest.raises(ValidationError):
            MoteurPersistence.update_lien(fichier_arbre_avec_lien, "l_001", {"type": "ami"})


class TestDeleteLien:
    """Tests pour la suppression d'un lien."""

    def test_supprimer_lien(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'un lien peut être supprimé (ex: en utilisant del ou une méthode dédiée).
        Indice : Si une liste de liens est utilisée, vérifier que le lien est retiré.
        """
        MoteurPersistence.delete_lien(fichier_arbre_avec_lien, "l_001")
        arbre_charge = MoteurPersistence.load(fichier_arbre_avec_lien)
        assert len(arbre_charge.liens) == 0

    def test_supprimer_lien_inexistant_echoue(self, fichier_arbre_avec_lien):
        """
        TODO: Vérifier qu'une erreur est levée si on tente de supprimer un lien inexistant.
        Indice : Utiliser pytest.raises() avec une exception appropriée (ex: ValueError).
        """
        MoteurPersistence.delete_lien(fichier_arbre_avec_lien, "l_999")
        arbre_charge = MoteurPersistence.load(fichier_arbre_avec_lien)
        assert len(arbre_charge.liens) == 1
