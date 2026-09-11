from src.models import GenealogicalTree, Person
from persistence import PersistenceEngine


def main() -> None:
    """Run a small persistence example."""
    person = Person(
        identifier="p_001",
        first_name="Ada",
        last_name="Lovelace",
    )
    tree = GenealogicalTree(people=[person], relationships=[])
    PersistenceEngine.dump(tree, "data/genealogical_tree.json")
    PersistenceEngine.load("data/genealogical_tree.json")


if __name__ == "__main__":
    main()
