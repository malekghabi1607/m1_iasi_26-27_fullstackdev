"""
Tests pour les opérations CRUD sur les liens.

Objectif : Tester les opérations unitaires sur les liens (création, lecture, mise à jour, suppression).
"""

import pytest
from pydantic import ValidationError

from src.models import Lien, LienType


class TestCreateLien:
    """Tests pour la création d'un lien."""

    def test_creer_lien_avec_champs_obligatoires(self):
        """Vérifie qu'un lien peut être créé avec les champs obligatoires (id, source, destination, type)"""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        assert lien.id == "1"
        assert lien.source == "p1"
        assert lien.destination == "p2"
        assert lien.type == LienType.PARENT

    def test_creer_lien_sans_id_echoue(self):
        """Vérifie qu'une ValidationError est levée si l'ID est manquant."""
        with pytest.raises(ValidationError): Lien(source="p1", destination="p2", type=LienType.PARENT)

    def test_creer_lien_sans_source_echoue(self):
        """Vérifie qu'une ValidationError est levée si la source est manquante."""
        with pytest.raises(ValidationError): Lien(id="1", destination="p2", type=LienType.PARENT)

    def test_creer_lien_sans_destination_echoue(self):
        """Vérifie qu'une ValidationError est levée si la destination est manquante."""
        with pytest.raises(ValidationError): Lien(id="1", source="p1", type=LienType.PARENT)

    def test_creer_lien_sans_type_echoue(self):
        """Vérifie qu'une ValidationError est levée si le type est manquant."""
        with pytest.raises(ValidationError): Lien(id="1", source="p1", destination="p2")

    def test_creer_lien_avec_type_invalide_echoue(self):
        """Vérifie qu'une ValidationError est levée si le type est invalide (ex: "ami")."""
        with pytest.raises(ValidationError): Lien(id="1", source="p1", destination="p2", type="ami")


class TestReadLien:
    """Tests pour la lecture des informations d'un lien."""

    def test_lire_lien_avec_id_valide_et_ressource_presente(self):
        """Vérifie qu'un lien peut être lu avec un ID valide et que la ressource existe."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        liens = {"1": lien}
        lien_lu = liens["1"]
        assert lien_lu.id == "1"
        assert lien_lu.source == "p1"
        assert lien_lu.destination == "p2"
        assert lien_lu.type == LienType.PARENT

    def test_lire_lien_avec_id_valide_et_ressource_manquante(self):
        """Vérifie qu'une erreur est levée si l'ID est valide mais que la ressource n'existe pas."""
        liens = {}
        with pytest.raises(KeyError): liens["1"]

    def test_lire_lien_avec_id_invalide(self):
        """Vérifie qu'une ValidationError est levée si l'ID est invalide (ex: None ou vide)."""
        with pytest.raises(ValidationError): Lien(id=None, source="p1", destination="p2", type=LienType.PARENT)


class TestUpdateLien:
    """Tests pour la mise à jour des informations d'un lien."""

    def test_mettre_a_jour_type_lien(self):
        """Vérifie qu'un lien peut être mis à jour avec un nouveau type valide."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        lien.type = LienType.PARTENAIRE
        assert lien.type == LienType.PARTENAIRE

    def test_mettre_a_jour_source_lien(self):
        """Vérifie qu'un lien peut être mis à jour avec une nouvelle source."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        lien.source = "p3"
        assert lien.source == "p3"

    def test_mettre_a_jour_destination_lien(self):
        """Vérifie qu'un lien peut être mis à jour avec une nouvelle destination."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT) 
        lien.destination = "p4"
        assert lien.destination == "p4"

    def test_mettre_a_jour_avec_type_invalide_echoue(self):
        """Vérifie qu'une ValidationError est levée si un type invalide est assigné."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        with pytest.raises(ValidationError): lien.type = "ami"


class TestDeleteLien:
    """Tests pour la suppression d'un lien."""

    def test_supprimer_lien(self):
        """Vérifie qu'un lien peut être supprimé (ex: en utilisant del ou une méthode dédiée)."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        liens = [lien]
        liens.remove(lien)
        assert lien not in liens

    def test_supprimer_lien_inexistant_echoue(self):
        """Vérifie qu'une erreur est levée si on tente de supprimer un lien inexistant."""
        lien = Lien(id="1", source="p1", destination="p2", type=LienType.PARENT)
        liens = []
        with pytest.raises(ValueError): liens.remove(lien)
