import pandas as pd
from sqlalchemy import Column, Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Sample(Base):
    __tablename__ = "sample"

    sample_id = Column("sample_id", Integer, primary_key=True)
    ptox_sample_id = Column("ptox_sample_id", String, nullable=False) # not unique, it's repeated for controls
    contrast_id = Column(Integer, ForeignKey("contrast.contrast_id", ondelete="CASCADE"))
    dose_id = Column("dose_id", Integer, ForeignKey("dose.dose_id"), nullable=False)
    group = Column("group", String, nullable=False)
    replicate = Column("replicate", Integer, nullable=False)

    # Many to One (Samples >>> Contrast)
    contrast = relationship("Contrast", back_populates="sample")
    # Many to One (Samples >>> Dose)
    sample_dose = relationship("Dose", back_populates="sample")
    # One to Many (Sample >>> Gene Counts)
    gene_count = relationship("GeneCount", back_populates="sample")
    # One to Many (Sample >>> Metabolite Intensities)
    metabolite_intensity = relationship("MetaboliteIntensity", back_populates="sample")

    __table_args__ = (
        Index("ix_sample_ptox_sample_id", ptox_sample_id),
        Index("ix_sample_dose_id", dose_id),
        UniqueConstraint(ptox_sample_id, contrast_id, name="uq_sample_ptox_sample_id_contrast_id")
    )
