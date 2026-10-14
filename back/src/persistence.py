import json
from pathlib import Path
from src.models import ArbreGenealogique


class MoteurPersistence:

    FICHIER = Path(__file__).parent.parent / '/data' / 'data.json'

    # === Globales sur l'arbre === #
    def dump(arbreGenealogique: ArbreGenealogique, file_path: str) -> None:
        """Écrit un arbre généalogique dans un fichier JSON, dans ../data."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(arbreGenealogique.model_dump_json(indent=2))

    def load(file_path: str) -> ArbreGenealogique:
        """Charge un fichier JSON et retourne un arbre généalogique."""
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")

        with open(file_path, 'r', encoding='utf-8') as f:
            return ArbreGenealogique.model_validate_json(f.read())

    # === CRUD Personnes === #
    def create_personne(personne_id):
        pass

    def get_personne(personne_id):
        pass

    def update_personne(personne_id):
        pass

    def delete_personne(personne_id):
        pass

    # === CRUD liens === #
    def create_lien(lien_id):
        pass

    def get_lien(lien_id):
        pass

    def update_lien(lien_id):
        pass

    def delete_lien(lien_id):
        pass