"""Persistence of the genealogy tree in a JSON file."""

from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from .models import FamilyTree
except ImportError:
    from models import FamilyTree


class TreePersistance:
    """Load and save an :class:`FamilyTree` as JSON."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> FamilyTree:
        """Take a json file path and return a FamilyTree."""
        if not self.path.exists():
            return FamilyTree(personnes=[], liens=[])

        with self.path.open("r", encoding="utf-8") as file:
            content = json.load(file)
        return FamilyTree.model_validate(content)

    def save(self, tree: FamilyTree) -> None:
        """Persist a validated tree atomically."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(f"{self.path.suffix}.tmp")
        content = tree.model_dump(mode="json")

        try:
            with temp.open("w", encoding="utf-8") as file:
                json.dump(content, file, ensure_ascii=False, indent=2)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            temp.replace(self.path)
        except Exception:
            temp.unlink(missing_ok=True)
            raise
