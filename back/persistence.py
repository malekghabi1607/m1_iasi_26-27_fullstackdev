"""Persistence of a genealogical tree in a JSON file."""

import os
from pathlib import Path

from src.models import GenealogicalTree


class MoteurPersistence:
    """Read and write validated genealogical trees as JSON."""

    @staticmethod
    def dump(tree: GenealogicalTree, file_path: str) -> None:
        """Write a genealogical tree to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(f"{path.suffix}.tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                file.write(tree.model_dump_json(indent=2))
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            temporary_path.replace(path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise

    @staticmethod
    def load(file_path: str) -> GenealogicalTree:
        """Read a JSON file and return a validated genealogical tree."""
        return GenealogicalTree.model_validate_json(
            Path(file_path).read_text(encoding="utf-8")
        )


PersistenceEngine = MoteurPersistence
