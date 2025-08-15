from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    ForeignKey,
    Index
)
from sqlalchemy.orm import relationship
from .base import Base


class ProteinMapping(Base):
    __tablename__ = "protein_mapping"

    mapping_id = Column("mapping_id", Integer, primary_key=True)
    external_id = Column("external_id", String, nullable=False)
    # Many to Many (External IDs >>> Protein)
    protein_id = Column("protein_id", Integer, ForeignKey("protein.protein_id"), nullable=False)
    protein = relationship("Protein", back_populates="idmapping")

    __table_args__ = (
        Index("ix_protein_mapping", protein_id),
        UniqueConstraint(external_id, protein_id, name="uq_protein_mapping_external_id_protein_id"),
    )
