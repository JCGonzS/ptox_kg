from sqlalchemy import Column, Integer, String, Boolean, Index
from sqlalchemy.orm import relationship
from .base import Base


class Chemical(Base):
    __tablename__ = "chemical"

    ptx_code = Column("ptx_code", Integer, primary_key=True)
    full_ptx_code = Column("full_ptx_code", String, nullable=False, unique=True)
    name = Column("name", String, nullable=False, unique=True)
    other_names = Column("other_names", String, nullable=True)
    selected = Column("selected", Boolean, nullable=False)
    # One to One (Chemical <> Chemical Information)
    information = relationship("ChemicalInformation", uselist=False, back_populates="chemical")
    # One to Many (Chemical >>> Chemical Association)
    association = relationship("ChemicalAssociation", back_populates="chemical")
    # One to Many (Chemical >>> Range-finding Experiment)
    range_finding = relationship("RangeFinding", back_populates="chemical")
    # One to Many (Chemical >>> Contrasts)
    contrast = relationship("Contrast", back_populates="chemical")

    __table_args__ = (
            Index("ix_chemical_full_ptx_code", full_ptx_code),
    )
    