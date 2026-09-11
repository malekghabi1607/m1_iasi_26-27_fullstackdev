"""Example of persisting and loading a genealogical tree."""

from pathlib import Path

from persistence import MoteurPersistence
from src.models import GenealogicalTree, Person


def main() -> None:
    """Write an example tree to JSON and load it again."""
    person = Person(
        identifier="p_001",
        first_name="Ada",
        last_name="Lovelace",
    )
    tree = GenealogicalTree(people=[person], relationships=[])
    file_path = Path("data/genealogical_tree.json")

    MoteurPersistence.dump(tree, str(file_path))
    loaded_tree = MoteurPersistence.load(str(file_path))
    print(f"Persistence round trip successful: {loaded_tree == tree}")


if __name__ == "__main__":
    main()
