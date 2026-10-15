import json
from pathlib import Path
from src.models import ArbreGenealogique, Personne, Lien
from pydantic import ValidationError


class MoteurPersistence:

    FICHIER = Path(__file__).parent.parent / 'data' / 'data.json'

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
    @staticmethod
    def create_personne(file_path: str, personne) -> ArbreGenealogique:
        """Ajoute une personne à l'arbre généalogique dans le fichier spécifié."""
        if not isinstance(personne, Personne):
            raise ValueError("L'argument 'personne' doit être une instance de Personne.")

        arbre = MoteurPersistence.load(file_path)

        if any(p.id == personne.id for p in arbre.personnes):
            raise ValueError('Il existe déjà une personne avec cet id')

        arbre.personnes.append(personne)
        MoteurPersistence.dump(arbre, file_path)
        return arbre

    @staticmethod
    def get_personne(file_path: str, personne_id: str) -> Personne:
        """Récupère une personne par son ID depuis le fichier spécifié."""
        arbre = MoteurPersistence.load(file_path)
        for personne in arbre.personnes:
            if personne.id == personne_id:
                return personne
        raise ValueError(f"Personne avec l'ID {personne_id} non trouvée.")

    @staticmethod
    def update_personne(file_path: str, personne_id: str, updates: dict) -> Personne:
        """Met à jour une personne par son ID dans le fichier spécifié avec un dictionnaire de mises à jour."""
        arbre = MoteurPersistence.load(file_path)

        # Trouver la personne à mettre à jour
        personne_index = None
        for i, personne in enumerate(arbre.personnes):
            if personne.id == personne_id:
                personne_index = i
                break

        if personne_index is None:
            raise ValueError(f"Personne avec l'ID {personne_id} non trouvée.")

        # Créer une copie de la personne avec les mises à jour
        personne_dict = arbre.personnes[personne_index].model_dump()
        personne_dict.update(updates)

        # Valider les données avec Pydantic
        try:
            personne_update = Personne(**personne_dict)
        except ValidationError as e:
            raise e

        # Mettre à jour l'arbre
        arbre.personnes[personne_index] = personne_update
        MoteurPersistence.dump(arbre, file_path)
        return personne_update

    @staticmethod
    def delete_personne(file_path: str, personne_id: str) -> None:
        """Supprime une personne par son ID dans le fichier spécifié."""
        arbre = MoteurPersistence.load(file_path)
        arbre.personnes = [p for p in arbre.personnes if p.id != personne_id]
        MoteurPersistence.dump(arbre, file_path)

    # === CRUD liens === #
    @staticmethod
    def create_lien(file_path: str, lien) -> ArbreGenealogique:
        """Ajoute un lien à l'arbre généalogique dans le fichier spécifié."""
        if not isinstance(lien, Lien):
            raise ValueError("L'argument 'lien' doit être une instance de Lien.")

        arbre = MoteurPersistence.load(file_path)

        if any(l.id == lien.id for l in arbre.liens):
            raise ValueError('Il existe déjà un lien avec cet id')

        arbre.liens.append(lien)
        MoteurPersistence.dump(arbre, file_path)
        return arbre

    def get_lien(file_path:str,lien_id):
        """Récupère un lien par son ID depuis le fichier spécifié."""
        arbre = MoteurPersistence.load(file_path)
        for lien in arbre.liens:
            if lien.id == lien_id:
                return lien
        raise ValueError(f"Lien avec l'ID {lien_id} non trouvée.")


    def update_lien(file_path: str, lien_id: str, updates: dict) -> Lien:
        """Met à jour un lien par son ID dans le fichier spécifié avec un dictionnaire de mises à jour."""
        arbre = MoteurPersistence.load(file_path)

        # Trouver la personne à mettre à jour
        lien_index = None
        for i, lien in enumerate(arbre.liens):
            if lien.id == lien_id:
                lien_index = i
                break

        if lien_index is None:
            raise ValueError(f"Lien avec l'ID {lien_id} non trouvée.")

        # Créer une copie de la personne avec les mises à jour
        lien_dict = arbre.liens[lien_index].model_dump()
        lien_dict.update(updates)

        # Valider les données avec Pydantic
        try:
            lien_update = Lien(**lien_dict)
        except ValidationError as e:
            raise e

        # Mettre à jour l'arbre
        arbre.liens[lien_index] = lien_update
        MoteurPersistence.dump(arbre, file_path)
        return lien_update

    def delete_lien(file_path:str,lien_id):
        """Supprime un lien par son ID dans le fichier spécifié."""
        arbre = MoteurPersistence.load(file_path)
        arbre.liens = [p for p in arbre.liens if p.id != lien_id]
        MoteurPersistence.dump(arbre, file_path)