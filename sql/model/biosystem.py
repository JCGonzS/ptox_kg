from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Biosystem(Base):
    __tablename__ = "biosystem"

    biosystem_id = Column("biosystem_id", Integer, primary_key=True)
    ptox_biosystem_code = Column("ptox_biosystem_code", String, nullable=False, unique=True)
    ptox_biosystem_name = Column("ptox_biosystem_name", String, nullable=False)
    ptox_partner_id = Column("ptox_partner_id", String, nullable=True)
    # Many to One (Biosystems >>> Organism)
    organism_id = Column(Integer, ForeignKey("organism.organism_id"), nullable=False)
    organism = relationship("Organism", back_populates="biosystem")
    # One to Many (Biosystem >>> Range Finding Experiments)
    range_finding = relationship("RangeFinding", back_populates="biosystem")
    # One to Many (Biosystem >>> Contrasts)
    contrast = relationship("Contrast", back_populates="biosystem")
    # One to Many (Biosystem >>> Phenotype Experiments)
    phenotype_experiment = relationship("Phenotype", back_populates="biosystem")
    # One to Many (Biosystem >>> Metabolites)
    metabolite = relationship("Metabolite", back_populates="biosystem")
    # One to Many (Biosystem >>> Timepoints)
    timepoint = relationship("Timepoint", back_populates="biosystem")
