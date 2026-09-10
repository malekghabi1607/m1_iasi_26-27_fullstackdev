"""Persistence of the genealogy tree in a JSON file."""

from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from .models import ArbreGenealogiqe
except ImportError:
    from models import ArbreGenealogiqe


class PersistanceArbre:
    """Load and save an :class:`ArbreGenealogiqe` as JSON."""

    def __init__(self, chemin: str | Path) -> None:
        self.chemin = Path(chemin)

    def charger(self) -> ArbreGenealogiqe:
        """Return the stored tree, or an empty tree when no file exists."""
        if not self.chemin.exists():
            return ArbreGenealogiqe(personnes=[], liens=[])

        with self.chemin.open("r", encoding="utf-8") as fichier:
            contenu = json.load(fichier)
        return ArbreGenealogiqe.model_validate(contenu)

    def sauvegarder(self, arbre: ArbreGenealogiqe) -> None:
        """Persist a validated tree atomically."""
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        temporaire = self.chemin.with_suffix(f"{self.chemin.suffix}.tmp")
        contenu = arbre.model_dump(mode="json")

        try:
            with temporaire.open("w", encoding="utf-8") as fichier:
                json.dump(contenu, fichier, ensure_ascii=False, indent=2)
                fichier.write("\n")
                fichier.flush()
                os.fsync(fichier.fileno())
            temporaire.replace(self.chemin)
        except Exception:
            temporaire.unlink(missing_ok=True)
            raise
