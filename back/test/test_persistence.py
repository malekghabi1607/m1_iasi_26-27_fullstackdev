import pytest
from pathlib import Path
from pydantic import ValidationError

from src.models import ArbreGenealogique
from src.persistence import MoteurPersistence


class TestDump:
    """Tests pour la fonction dump de MoteurPersistence."""

    def test_dump_ecrit_le_json_dans_le_fichier(self, tmp_path, arbre_valide):
        """Vérifie que dump écrit correctement un arbre valide dans un fichier."""
        file_path = tmp_path / "arbre.json"

        MoteurPersistence.dump(arbre_valide, str(file_path))

        assert file_path.exists()
        contenu = file_path.read_text(encoding="utf-8")
        assert "personnes" in contenu
        assert "liens" in contenu

    def test_dump_leve_une_erreur_avec_arbre_invalide(
        self, tmp_path, arbre_invalide_sans_personnes
    ):
        """Vérifie que dump lève une ValidationError si l'arbre est invalide."""
        with pytest.raises(ValidationError):
            arbre = ArbreGenealogique(**arbre_invalide_sans_personnes)
            MoteurPersistence.dump(arbre, str(file_path))


class TestLoad:
    """Tests pour la fonction load de MoteurPersistence."""

    def test_load_retourne_l_arbre_valide(self, tmp_path):
        """Vérifie que load charge correctement un fichier JSON valide."""
        file_path = tmp_path / "arbre.json"
        contenu = '{"personnes": [], "liens": []}'
        file_path.write_text(contenu, encoding="utf-8")

        resultat = MoteurPersistence.load(str(file_path))

        assert isinstance(resultat, ArbreGenealogique)
        assert resultat.personnes == []
        assert resultat.liens == []

    def test_load_leve_une_erreur_si_le_fichier_n_existe_pas(self, tmp_path):
        """Vérifie que load lève FileNotFoundError si le fichier n'existe pas."""
        file_path = tmp_path / "inexistant.json"

        with pytest.raises(FileNotFoundError, match="n'existe pas"):
            MoteurPersistence.load(str(file_path))

    def test_load_leve_une_erreur_si_le_contenu_est_invalide(self, tmp_path):
        """Vérifie que load lève ValidationError si le contenu JSON est invalide."""
        file_path = tmp_path / "arbre_invalide.json"
        contenu = '{"personnes": []}'
        file_path.write_text(contenu, encoding="utf-8")

        with pytest.raises(ValidationError):
            MoteurPersistence.load(str(file_path))

def test_fichier_pointe_vers_data_json_du_projet():
    """Vérifie que FICHIER pointe vers back/data/data.json."""
    attendu = Path(__file__).parent.parent / "data" / "data.json"

    assert MoteurPersistence.FICHIER == attendu
