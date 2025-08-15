from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from .base import Base


class MetaboliteDifferential(Base):
    __tablename__ = "metabolite_differential"

    measurement_id = Column("measurement_id", Integer, primary_key=True)
    contrast_id = Column(
        "contrast_id",
        Integer,
        ForeignKey("contrast.contrast_id", ondelete="CASCADE"),
        nullable=False,
    )
    assay_id = Column("assay_id", Integer, ForeignKey("metabolomics_assay.assay_id"), nullable=False)
    metabolite_id = Column(
        "metabolite_id", String, nullable=False
        # "metabolite_id", String, ForeignKey("metabolite.metabolite_id"), nullable=False
    )
    estimate = Column("estimate", Float, nullable=True)
    pvalue = Column("pvalue", Float, nullable=True)
    padj = Column("padj", Float, nullable=True)
    ratio = Column("ratio", Float, nullable=True)

    # Many to One (Metabolite Differential >>> Contrast)
    contrast = relationship("Contrast", back_populates="metabolite_differential")
    # Many to One (Metabolite Intensities >>> Assay)
    assay = relationship("MetabolomicsAssay", back_populates="metabolite_differential")

    __table_args__ = (
        Index("ix_metabolite_differential_metabolite_id", metabolite_id),
        Index("ix_metabolite_differential_contrast_id", contrast_id),
        Index("ix_metabolite_differential_contrast_assay", contrast_id, assay_id),
    )

