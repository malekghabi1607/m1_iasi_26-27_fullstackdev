"""Persistence of a genealogical tree in a JSON file."""

from pathlib import Path

from src.models import GenealogicalTree


class PersistenceEngine:
    """Read and write validated genealogical trees as JSON."""

    @staticmethod
    def dump(tree: GenealogicalTree, file_path: str) -> None:
        """Write a genealogical tree to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(tree.model_dump_json(indent=2), encoding="utf-8")

    @staticmethod
    def load(file_path: str) -> GenealogicalTree:
        """Read a JSON file and return a validated genealogical tree."""
        return GenealogicalTree.model_validate_json(
            Path(file_path).read_text(encoding="utf-8")
        )
