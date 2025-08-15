from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from .base import Base
from .ortholog import Ortholog


class Protein(Base):
    __tablename__ = "protein"

    protein_id = Column("protein_id", Integer, primary_key=True)
    uniprot_ac = Column("uniprot_ac", String(12), nullable=False, unique=True)
    uniprot_id = Column("uniprot_id", String(25), nullable=False, unique=True)
    gene_name = Column("gene_name", String, nullable=True)
    protein_name = Column("protein_name", String, nullable=True)
    status = Column("status", String(12), nullable=True)
    seq_length = Column("seq_length", Integer, nullable=True)
    sequence = Column("sequence", String, nullable=True)
    # Many to One (Proteins >>> Organism)
    organism_id = Column(Integer, ForeignKey("organism.organism_id"), nullable=False)
    organism = relationship("Organism", back_populates="protein")
    # One to Many (Protein >>> Synonyms)
    synonym = relationship("ProteinSynonym", back_populates="protein")
    # One to Many (Protein >>> Annotations)
    annotation = relationship("ProteinAnnotation", back_populates="protein")
    # One to Many (Protein >>> ID Mappings)
    idmapping = relationship("ProteinMapping", back_populates="protein")
    # One to Many (Protein >>> Ortholog Proteins A/B)
    ortholog_a = relationship(
        "Ortholog", back_populates="protein_a", foreign_keys=[Ortholog.protein_id_a]
    )
    ortholog_b = relationship(
        "Ortholog", back_populates="protein_b", foreign_keys=[Ortholog.protein_id_b]
    )

    __table_args__ = (
        Index("ix_protein_gene_name", gene_name),
        Index("ix_protein_organism_id", organism_id),
    )
