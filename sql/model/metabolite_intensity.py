from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    Index,
    UniqueConstraint

)
from sqlalchemy.orm import relationship
from .base import Base


class MetaboliteIntensity(Base):
    __tablename__ = "metabolite_intensity"

    measurement_id = Column("measurement_id", Integer, primary_key=True)
    sample_id = Column(
        "sample_id", Integer, ForeignKey("sample.sample_id", ondelete="CASCADE"), nullable=False
    )
    assay_id = Column("assay_id", Integer, ForeignKey("metabolomics_assay.assay_id"), nullable=False)
    metabolite_id = Column("metabolite_id", Integer,
        # ForeignKey("metabolite.metabolite_id"),
        nullable=False
    )
    intensity = Column("expression", Float, nullable=False)

    # Many to One (Metabolite Intensities >>> Sample)
    sample = relationship("Sample", back_populates="metabolite_intensity")
    # Many to One (Metabolite Intensities >>> Assay)
    assay = relationship("MetabolomicsAssay", back_populates="metabolite_intensity")

    __table_args__ = (
        Index("ix_metabolite_intensity_sample_id", sample_id),
        # UniqueConstraint(assay_id, sample_id, metabolite_id, name="uq_metabolite_intensity_sample_metabolite"),
    )
