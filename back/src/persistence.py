import json
from pathlib import Path
from src.models import ArbreGenealogiqe


class MoteurPersistence:
	def dump(arbreGenealogique: ArbreGenealogiqe) -> None:
		"""Écrit un arbre généalogique dans un fichier JSON, dans ../data."""
		FICHIER = Path(__file__).parent.parent / 'data' / 'data.json'
		with open(FICHIER, 'w', encoding='utf-8') as f:
			json.dump(arbreGenealogique.__dict__, f, ensure_ascii=False, indent=2)


	def load(selfnomFichier: str) -> ArbreGenealogiqe:
		"""Charge un fichier JSON et retourne un arbre généalogique."""
		#TODO

