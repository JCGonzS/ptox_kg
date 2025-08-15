from sqlalchemy import Column, Integer, String, UniqueConstraint, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from .base import Base


class GeneCount(Base):
    __tablename__ = "gene_count"

    measurement_id = Column("measurement_id", Integer, primary_key=True)
    sample_id = Column(
        "sample_id", Integer, ForeignKey("sample.sample_id", ondelete="CASCADE"), nullable=False
    )
    gene = Column("gene", String, nullable=False)
    normalized_count = Column("normalized_count", Float, nullable=False)

    # Many to One (Gene Counts >>> Sample)
    sample = relationship("Sample", back_populates="gene_count")

    __table_args__ = (
        Index("ix_gene_count_sample_id", sample_id),
        UniqueConstraint(sample_id, gene, name="uq_gene_count_sample_id_gene")
    )
