from sqlalchemy import (
    Column,
    Integer,
    Float,
    UniqueConstraint,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from .base import Base


class Ortholog(Base):
    __tablename__ = "ortholog"

    ortholog_id = Column("ortholog_id", Integer, primary_key=True)
    # Many to One (Ortholog Protein A/B >>> Protein)
    protein_id_a = Column("protein_id_a", Integer, ForeignKey("protein.protein_id"), nullable=False)
    protein_a = relationship("Protein", back_populates="ortholog_a", foreign_keys=[protein_id_a])
    protein_id_b = Column("protein_id_b", Integer, ForeignKey("protein.protein_id"), nullable=False)
    protein_b = relationship("Protein", back_populates="ortholog_b", foreign_keys=[protein_id_b])
    score = Column("score", Float, nullable=False)

    __table_args__ = (
        Index("ix_ortholog_protein_a", protein_id_a),
        Index("ix_ortholog_protein_b", protein_id_b),
        UniqueConstraint(protein_id_a, protein_id_b, name="uq_ortholog_protein_pair_ab"),
        UniqueConstraint(protein_id_b, protein_id_a, name="uq_ortholog_protein_pair_ba")
    )
