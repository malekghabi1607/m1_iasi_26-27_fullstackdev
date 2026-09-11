from enum import Enum
from typing import List, Optional

from pydantic import AliasChoices, BaseModel, Field


class Person(BaseModel):
    """A person and their basic biographical information."""

    identifier: str = Field(
        ...,
        validation_alias=AliasChoices("identifier", "id", "identifiant"),
        description="Unique identifier for the person.",
    )
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_birth: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}(-\d{2}-\d{2})?$",
        description="A year or a full ISO 8601 date.",
    )
    place_of_death: Optional[str] = None
    date_of_death: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}(-\d{2}-\d{2})?$",
        description="A year or a full ISO 8601 date.",
    )
    nationality: Optional[str] = None


class RelationshipType(str, Enum):
    """Allowed relationship types in a genealogical tree."""

    PARENT = "parent"
    PARTNER = "partner"


class Relationship(BaseModel):
    """A relationship between two people."""

    id: str = Field(..., description="Unique identifier for the relationship.")
    source: str = Field(..., description="ID of the source person.")
    destination: str = Field(..., description="ID of the destination person.")
    type: RelationshipType = Field(
        ..., description="Type of relationship between the two people."
    )


class GenealogicalTree(BaseModel):
    """A complete genealogical tree."""

    people: List[Person] = Field(
        ..., description="People included in the genealogical tree."
    )
    relationships: List[Relationship] = Field(
        ..., description="Relationships between people."
    )
