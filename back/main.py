from src.models import GenealogicalTree, Person
from persistence import MoteurPersistence


def main() -> None:
    """Run a small persistence example."""
    person = Person(
        identifier="p_001",
        first_name="Ada",
        last_name="Lovelace",
    )
    tree = GenealogicalTree(people=[person], relationships=[])
    MoteurPersistence.dump(tree, "data/genealogical_tree.json")
    MoteurPersistence.load("data/genealogical_tree.json")


if __name__ == "__main__":
    main()
