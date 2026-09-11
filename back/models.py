from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class Person(BaseModel):
    """
    A person and their base biographic informations.

    Attributes:
        id (str): unique person's id (ex. : 'p_001'). Required.
        last_name (str): The person's last name. None by default.
        first_name (str): The person's first name. None by default.
        place_of_birth (str): The person's place of birth. None by default.
        date_of_birth (Optional[str]): The date of birth. Can be on full 
            format ISO 8601 (AAAA-MM-JJ) or only year (AAAA). None by default.
        place_of_death (str): The person's place of death. None by default
        date_of_death (Optional[str]): The date of death. Can be on full
            format ISO 8601 (AAAA-MM-JJ) or only year (AAAA). None by default.
        Nationality (Optional[str]): The person's nationality. None by default.
    """
    id: str = Field(..., description="Unique identifier for the person (e.g., 'p_001').")
    last_name: str
    first_name: str
    place_of_birth: str
    date_of_birth: Optional[str] = Field(
        default=None, 
        pattern=r"^\d{4}(-\d{2}-\d{2})?$", 
        description="Allows full ISO date or just the year."
    )
    place_of_death: str
    date_of_death: Optional[str] = Field(
        default=None, 
        pattern=r"^\d{4}(-\d{2}-\d{2})?$", 
        description="Allows full ISO date or just the year."
    )
    nationality: Optional[str]


class LinkType(str, Enum):
    """Enumeration of allowed relationship types within the family tree.

    Attributes:
        BIOLOGICAL_PARENT (str): A biological parent-child connection.
        ADOPTIVE_PARENT (str): An adoptive parent-child connection.
        STEP_PARENT (str): A step-parent-child connection.
        FOSTER_PARENT (str): A foster parent-child connection.
        PARTNER (str): A formal partnership between peers.
    """
    PARENT = "parent"
    PARTNER = "partner"


class Link(BaseModel):
    """Represents a relationship edge between two individuals.

    Attributes:
        id (str): Unique identifier for the relationship link.
        source (str): ID of the source node.
        target (str): ID of the target node.
        type (LinkType): The explicit type of relationship.
        start_date (Optional[str]): ISO 8601 date representing when the relationship began.
        end_date (Optional[str]): ISO 8601 date representing when the relationship ended.
        notes (Optional[str]): Additional context.
        events (Optional[List[Event]]): Significant events related to the relationship.
    """
    id: str = Field(..., description="Unique identifier for the relationship link (e.g., 'l_001').")
    source: str = Field(..., description="ID of the source node.")
    destination: str = Field(..., description="ID of the target node.")
    type: LinkType = Field(..., description="The explicit type of relationship connecting the source and target.")


class FamilyTree(BaseModel):
    """The complete Family Tree graph structure.

    Attributes:
        nodes (List[Node]): List of individuals.
        links (List[Link]): List of relationships.
    """
    persons: List[Person] = Field(..., description="List of individuals (entities) in the family tree.")
    liens: List[Link] = Field(..., description="List of relationships (edges) between individuals.")
