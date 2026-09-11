import json
from pathlib import Path
from src.models import ArbreGenealogique


class MoteurPersistence:

	FICHIER = Path(__file__).parent.parent / 'data' / 'data.json'

	def dump(arbreGenealogique: ArbreGenealogique, file_path: str) -> None:
		"""Écrit un arbre généalogique dans un fichier JSON, dans ../data."""
		with open(file_path, 'w', encoding='utf-8') as f:
			f.write(arbreGenealogique.model_dump_json(indent=2))


	def load(file_path: str) -> ArbreGenealogique:
		"""Charge un fichier JSON et retourne un arbre généalogique."""
		with open(file_path, 'r', encoding='utf-8') as f:
			return ArbreGenealogique.model_validate_json(f.read())

