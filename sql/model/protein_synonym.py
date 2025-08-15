from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from .base import Base


class ProteinSynonym(Base):
    __tablename__ = "protein_synonym"

    synonym_id = Column("synonym_id", Integer, primary_key=True)
    synonym = Column("synonym", String, nullable=False)
    source_database = Column("source_database", String, nullable=False)
    # Many to One (Synonyms >>> Protein)
    protein_id = Column("protein_id", Integer, ForeignKey("protein.protein_id"), nullable=False)
    protein = relationship("Protein", back_populates="synonym")

    __table_args__ = (
        UniqueConstraint(protein_id, synonym, name="uq_protein_synonym_protein_id_synonym"),
        Index("ix_protein_synonym_protein_id", protein_id),
        Index("ix_protein_synonym_database", source_database),
    )
