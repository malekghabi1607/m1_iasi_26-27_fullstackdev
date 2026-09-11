from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class Personne(BaseModel):
    """
    Représente une personne avec ses informations biographiques de base.

    Attributes:
        id (str): Identifiant unique de la personne (ex. : 'p_001'). Requis.
        nom_famille (str): Le nom de famille de la personne. Requis.
        prenom (str): Le prénom de la personne. Requis.
        lieu_naissance (str): Le lieu de naissance de la personne. Requis.
        date_naissance (Optional[str]): La date de naissance. Peut être au format 
            complet ISO 8601 (AAAA-MM-JJ) ou juste l'année (AAAA). Par défaut à None.
        lieu_mort (str): Le lieu de décès de la personne. Requis.
        date_mort (Optional[str]): La date de décès. Peut être au format 
            complet ISO 8601 (AAAA-MM-JJ) ou juste l'année (AAAA). Par défaut à None.
        nationalite (Optional[str]): La nationalité de la personne. Par défaut à None.
    """
    id: str = Field(..., description="Unique identifier for the person (e.g., 'p_001').")
    nom_famille: Optional[str] = None
    prenom: Optional[str] = None
    lieu_naissance: Optional[str] = None
    date_naissance: Optional[str] = Field(
        default=None, 
        pattern=r"^\d{4}(-\d{2}-\d{2})?$", 
        description="Allows full ISO date or just the year."
    )
    lieu_mort: Optional[str] = None
    date_mort: Optional[str] = Field(
        default=None, 
        pattern=r"^\d{4}(-\d{2}-\d{2})?$", 
        description="Allows full ISO date or just the year."
    )
    nationalite: Optional[str] = None


class LienType(str, Enum):
    """Enumeration of allowed relationship types within the family tree.

    Attributes:
        BIOLOGICAL_PARENT (str): A biological parent-child connection.
        ADOPTIVE_PARENT (str): An adoptive parent-child connection.
        STEP_PARENT (str): A step-parent-child connection.
        FOSTER_PARENT (str): A foster parent-child connection.
        PARTNER (str): A formal partnership between peers.
    """
    PARENT = "parent"
    PARTENAIRE = "partenaire"


class Lien(BaseModel):
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
    type: LienType = Field(..., description="The explicit type of relationship connecting the source and target.")


class ArbreGenealogique(BaseModel):
    """The complete Family Tree graph structure.

    Attributes:
        nodes (List[Node]): List of individuals.
        links (List[Link]): List of relationships.
    """
    personnes: List[Personne] = Field(..., description="List of individuals (entities) in the family tree.")
    liens: List[Lien] = Field(..., description="List of relationships (edges) between individuals.")
