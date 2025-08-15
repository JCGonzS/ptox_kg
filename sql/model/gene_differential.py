from sqlalchemy import Column, Integer, String, Float, UniqueConstraint,ForeignKey, Index
from sqlalchemy.orm import relationship
from .base import Base


class GeneDifferential(Base):
    __tablename__ = "gene_differential"

    measurement_id = Column("measurement_id", Integer, primary_key=True)
    contrast_id = Column(
        "contrast_id",
        Integer,
        ForeignKey("contrast.contrast_id", ondelete="CASCADE"),
        nullable=False,
    )
    gene = Column("gene", String, nullable=False)
    log2_fc = Column("log2_fc", Float, nullable=False)
    lfcse = Column("lfcse", Float, nullable=False)
    pvalue = Column("pvalue", Float, nullable=False)
    padj = Column("padj", Float, nullable=True)

    # Many to One (Gene Differential Expression >>> Contrast)
    contrast = relationship("Contrast", back_populates="gene_differential_exp")

    __table_args__ = (
        Index("ix_gene_differential_gene", "gene"),
        Index("ix_gene_differential_contrast_id", "contrast_id"),
        UniqueConstraint(gene, contrast_id, name="uq_gene_differential_gene_contrast_id"),
    )
