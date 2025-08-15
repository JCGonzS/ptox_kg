from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Dose(Base):
    __tablename__ = "dose"

    dose_id = Column("dose_id", Integer, primary_key=True)
    dose_code = Column("dose_code", String(2), nullable=False, unique=True)
    dose_name = Column("dose_name", String, nullable=False, unique=True)
    # One to Many (Dose >>> Contrasts)
    contrast = relationship("Contrast", back_populates="treatment_dose")
    # One to Many (Dose >>> Samples)
    sample = relationship("Sample", back_populates="sample_dose")
