"""
Tests des règles de cohérence de l'arbre généalogique.

Objectif : refuser les données qui ont le bon format mais qui n'ont pas de sens
(lien vers soi-même, boucle dans les ancêtres, trois parents, etc.).
"""

import pytest
from pydantic import ValidationError

from src.models import ArbreGenealogique, Lien, LienType, Personne
from src.persistence import MoteurPersistence, RegleMetierError


@pytest.fixture
def fichier_famille(tmp_path):
    """Une petite famille : un père, une mère, leur enfant, et deux autres personnes."""
    arbre = ArbreGenealogique(
        personnes=[
            Personne(id="pere", prenom="Jean", date_naissance="1960"),
            Personne(id="mere", prenom="Marie", date_naissance="1962-03-10"),
            Personne(id="enfant", prenom="Paul", date_naissance="1990-07-01"),
            Personne(id="autre", prenom="Léa", date_naissance="1995"),
            Personne(id="sans_date", prenom="Max"),
        ],
        liens=[
            Lien(id="l_1", source="pere", destination="enfant", type=LienType.PARENT),
            Lien(id="l_2", source="mere", destination="enfant", type=LienType.PARENT),
            Lien(id="l_3", source="pere", destination="mere", type=LienType.PARTENAIRE),
        ],
    )
    file_path = tmp_path / "famille.json"
    MoteurPersistence.dump(arbre, file_path)
    return file_path


def nouveau_lien(lien_id, source, destination, type_lien):
    return Lien(id=lien_id, source=source, destination=destination, type=type_lien)


class TestReglesCreationLien:
    """Règles vérifiées quand on crée un lien."""

    def test_lien_valide_accepte(self, fichier_famille):
        MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "enfant", "autre", LienType.PARENT))

        assert MoteurPersistence.get_lien(fichier_famille, "l_9").destination == "autre"

    def test_refuse_une_personne_inexistante(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="existantes"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "pere", "fantome", LienType.PARENT))

    def test_refuse_un_lien_vers_soi_meme(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="elle-même"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "autre", "autre", LienType.PARTENAIRE))

    def test_refuse_un_lien_parent_en_double(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="existe déjà"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "pere", "enfant", LienType.PARENT))

    def test_refuse_un_partenariat_en_double_dans_l_autre_sens(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="existe déjà"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "mere", "pere", LienType.PARTENAIRE))

    def test_refuse_plus_de_deux_parents(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="deux parents"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "sans_date", "enfant", LienType.PARENT))

    def test_refuse_qu_un_enfant_soit_parent_de_son_parent(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="propre ancêtre"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "enfant", "pere", LienType.PARENT))

    def test_refuse_une_boucle_sur_plusieurs_generations(self, fichier_famille):
        # enfant -> sans_date : sans_date devient le petit-enfant du père
        MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_8", "enfant", "sans_date", LienType.PARENT))

        with pytest.raises(RegleMetierError, match="propre ancêtre"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "sans_date", "pere", LienType.PARENT))

    def test_refuse_un_parent_ne_apres_son_enfant(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="né avant"):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "autre", "pere", LienType.PARENT))

    def test_lien_refuse_n_est_pas_enregistre(self, fichier_famille):
        with pytest.raises(RegleMetierError):
            MoteurPersistence.create_lien(fichier_famille, nouveau_lien("l_9", "autre", "autre", LienType.PARTENAIRE))

        assert len(MoteurPersistence.load(fichier_famille).liens) == 3


class TestReglesModificationLien:
    """Les mêmes règles s'appliquent quand on modifie un lien."""

    def test_refuse_une_modification_vers_soi_meme(self, fichier_famille):
        with pytest.raises(RegleMetierError, match="elle-même"):
            MoteurPersistence.update_lien(fichier_famille, "l_1", {"destination": "pere"})

    def test_un_lien_ne_se_compte_pas_lui_meme_comme_doublon(self, fichier_famille):
        MoteurPersistence.update_lien(fichier_famille, "l_3", {"type": LienType.PARTENAIRE})

        assert MoteurPersistence.get_lien(fichier_famille, "l_3").type == LienType.PARTENAIRE


class TestSuppressionPersonne:
    """Supprimer une personne doit supprimer ses liens."""

    def test_supprimer_une_personne_supprime_ses_liens(self, fichier_famille):
        MoteurPersistence.delete_personne(fichier_famille, "pere")

        arbre = MoteurPersistence.load(fichier_famille)
        assert [l.id for l in arbre.liens] == ["l_2"]


class TestDatesPersonne:
    """Une personne ne peut pas mourir avant d'être née."""

    def test_refuse_un_deces_avant_la_naissance(self):
        with pytest.raises(ValidationError, match="décès"):
            Personne(id="p", date_naissance="1990-05-15", date_mort="1980")

    def test_accepte_naissance_et_deces_la_meme_annee(self):
        personne = Personne(id="p", date_naissance="1990", date_mort="1990-12-31")

        assert personne.date_mort == "1990-12-31"

    def test_refuse_une_modification_qui_rend_les_dates_incoherentes(self):
        personne = Personne(id="p", date_naissance="1990")

        with pytest.raises(ValidationError, match="décès"):
            personne.date_mort = "1950"
