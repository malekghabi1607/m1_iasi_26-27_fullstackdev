import json
from pathlib import Path
from src.models import ArbreGenealogiqe


class MoteurPersistence:

	FICHIER = Path(__file__).parent.parent / 'data' / 'data.json'

	def dump(arbreGenealogique: ArbreGenealogiqe) -> None:
		"""Écrit un arbre généalogique dans un fichier JSON, dans ../data."""
		print(f"Dans dump, voici l'arbre généalogique : {arbreGenealogique}")
		with open(MoteurPersistence.FICHIER, 'w', encoding='utf-8') as f:
			f.write(arbreGenealogique.model_dump_json(indent=2))


	def load(file_path: str) -> ArbreGenealogiqe:
		"""Charge un fichier JSON et retourne un arbre généalogique."""
		with open(file_path, 'r', encoding='utf-8') as f:
			return ArbreGenealogiqe.model_validate_json(f.read())

