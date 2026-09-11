"""Persistence of a genealogical tree in a JSON file."""

import os
import json
from pathlib import Path

from src.models import ArbreGenealogique


class MoteurPersistence:
    """Read and write validated genealogical trees as JSON."""

    @staticmethod
    def dump(tree: ArbreGenealogique, file_path: str) -> None:
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
    def load(file_path: str) -> ArbreGenealogique:
        """Read a JSON file and return a validated genealogical tree."""
        return ArbreGenealogique.model_validate_json(
            Path(file_path).read_text(encoding="utf-8")
        )
        
    @staticmethod
    def read(file_path: str) :
        """Read a JSON file and return it's content"""
        with open(Path(file_path),'r') as file :
            data = json.load(file)
            return data


PersistenceEngine = MoteurPersistence
