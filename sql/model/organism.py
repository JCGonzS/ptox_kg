from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .ortholog import Ortholog


class Organism(Base):
    __tablename__ = "organism"

    organism_id = Column("organism_id", Integer, primary_key=True)
    scientific_name = Column("scientific_name", String, nullable=False, unique=True)
    common_name = Column("common_name", String, nullable=True, unique=True)
    uniprot_acronym = Column("uniprot_acronym", String, nullable=True, unique=True)
    ncbi_tax_id = Column("ncbi_tax_id", Integer, nullable=False, unique=True)
    division = Column("division", String, nullable=True)
    tax_lineage = Column("tax_lineage", String, nullable=True)
    # One to Many (Organism >>> Biosystems)
    biosystem = relationship("Biosystem", back_populates="organism")
    # One to Many (Organism >>> Proteins)
    protein = relationship("Protein", back_populates="organism")
    