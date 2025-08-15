from sqlalchemy import (
    Column,
    Integer,
    String,
    Index,

)
from sqlalchemy.orm import relationship
from .base import Base


class MetabolomicsAssay(Base):
    __tablename__ = "metabolomics_assay"

    assay_id = Column("assay_id", Integer, primary_key=True)
    assay_name = Column("assay_name", String, nullable=False, unique=True)
    assay_description = Column("assay_description", String, nullable=True)

    # One to Many (Assay >>> Metabolite Intensities)
    metabolite_intensity = relationship("MetaboliteIntensity", back_populates="assay")
    # One to Many (Assay >>> Metabolite Differential)
    metabolite_differential = relationship("MetaboliteDifferential", back_populates="assay")
    # One to Many (Assay >>> Metabolites)
    metabolite = relationship("Metabolite", back_populates="assay")
