from src.models import GenealogicalTree, Person, Relationship, RelationshipType
from persistence import PersistenceEngine


def main() -> None:
    """Run a small persistence example."""
    test = Person.model_validate({'identifier': '123', 'first_name': 'AAA', 'last_name': 'BBB', 'place_of_birth':'Here', 'date-of-birth': '2026-09-11', 'place-of-death':None, 'date-of-death':None, 'nationality':'FR'})
    print(test)
    person = Person(
        identifier="p_001",
        first_name="Ada",
        last_name="Lovelace",
    )
    person2 = Person(
        identifier="p_002",
        first_name="Some",
        last_name="Name",
    )
    
    relationship = Relationship(
        id = "r_001",
        source = person.identifier,
        destination = person2.identifier,
        type = RelationshipType("parent")
    )
    
    test2 = Relationship.model_validate({'id': "r_001", 'source': person.identifier, 'destination' : person2.identifier, 'type' : RelationshipType("parent")})
    print(test2)
    
    tree = GenealogicalTree(people=[person,person2], relationships=[relationship])
    PersistenceEngine.dump(tree, "data/genealogical_tree.json")
    PersistenceEngine.load("data/genealogical_tree.json")


if __name__ == "__main__":
    main()
