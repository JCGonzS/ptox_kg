from sqlalchemy import Column, Integer, String, ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.orm import relationship
from .base import Base


class ProteinAnnotation(Base):
    __tablename__ = "protein_annotation"

    annotation_id = Column("annotation_id", Integer, primary_key=True)
    annotation = Column("annotation", String, nullable=False)
    annotation_hash = Column(String(32), nullable=False)  # md5 hash
    source_database: str = Column("source_database", String, nullable=False)
    # Many to Many (Annotations >>> Proteins)
    protein_id = Column("protein_id", Integer, ForeignKey("protein.protein_id"), nullable=False)
    protein = relationship("Protein", back_populates="annotation")

    __table_args__ = (
        Index("ix_protein_annotation_protein_id", protein_id),
        Index("ix_protein_annotation_protein_id_source_database", protein_id, source_database),
        UniqueConstraint(protein_id, annotation_hash, name="uq_protein_annotation_protein_id_hash"),
    )
