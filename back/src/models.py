from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class Personne(BaseModel):
    """
    Représente une personne avec ses informations biographiques de base.

    Attributes:
        id (str): Identifiant unique de la personne (ex. : 'p_001'). Requis.
            Ne peut pas être vide (min_length=1) car il sert à relier
            les personnes entre elles via les liens.
        nom_famille (Optional[str]): Le nom de famille. Par défaut à None.
        prenom (Optional[str]): Le prénom. Par défaut à None.
        lieu_naissance (Optional[str]): Le lieu de naissance. Par défaut à None.
        date_naissance (Optional[str]): La date de naissance, au format
            AAAA-MM-JJ ou AAAA. Par défaut à None.
        lieu_mort (Optional[str]): Le lieu de décès. Par défaut à None.
        date_mort (Optional[str]): La date de décès, au format
            AAAA-MM-JJ ou AAAA. Par défaut à None.
        nationalite (Optional[str]): La nationalité. Par défaut à None.
    """
      # revalide les champs à chaque modification
    model_config = ConfigDict(validate_assignment=True)


    # min_length=1 : refuse un id vide ("") car l'id sert à relier les personnes via les liens
    id: str = Field(...,  min_length=1 , description="Unique identifier for the person (e.g., 'p_001').")
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
