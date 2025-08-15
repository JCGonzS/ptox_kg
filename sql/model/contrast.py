from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


class Contrast(Base):
    __tablename__ = "contrast"

    contrast_id = Column("contrast_id", Integer, primary_key=True)
    ptox_contrast_id = Column("ptox_contrast_id", String, nullable=False, unique=True)
    biosystem_id = Column("biosystem_id", Integer, ForeignKey("biosystem.biosystem_id"), nullable=False)
    ptx_code = Column("ptx_code", Integer, ForeignKey("chemical.ptx_code"), nullable=False)
    batch = Column("batch", String, nullable=False)
    solvent_id = Column("solvent", Integer, ForeignKey("solvent.solvent_id"), nullable=False)
    timepoint_id = Column("timepoint_id", Integer, ForeignKey("timepoint.timepoint_id"), nullable=False)
    treatment_dose_id = Column("treatment_dose_id", Integer, ForeignKey("dose.dose_id"), nullable=False)
    # file_id = Column("file_id", Integer, ForeignKey("file.file_id"), nullable=False, unique=True)
 
    # Many to One (Contrasts >>> Biosystem)
    biosystem = relationship("Biosystem", back_populates="contrast")
    # Many to One (Contrasts >>> Chemical)
    chemical = relationship("Chemical", back_populates="contrast")
    # Many to One (Contrasts >>> Solvent)
    solvent = relationship("Solvent", back_populates="contrast")
    # Many to One (Contrasts >>> Dose)
    treatment_dose = relationship("Dose", back_populates="contrast")
    # Many to One (Contrasts >>> Timepoint)
    timepoint = relationship("Timepoint", back_populates="contrast")
    
    # One to Many (Contrast >>> Samples)
    sample = relationship("Sample", back_populates="contrast")
    # One to Many (Contrast >>> Gene Differential Expression)
    gene_differential_exp = relationship("GeneDifferential", back_populates="contrast")
    # One to Many (Contrast >>> Metabolite Differential)
    metabolite_differential = relationship("MetaboliteDifferential", back_populates="contrast")

    # file = relationship("File", back_populates="rnaseq_contrast_pilot")

    __table_args__ = (
        Index("ix_contrast_biosystem_id", biosystem_id),
        Index("ix_contrast_ptx_code", ptx_code),
        Index("ix_contrast_timepoint_id", timepoint_id),
        Index("ix_contrast_treatment_dose_id", treatment_dose_id)
    )
