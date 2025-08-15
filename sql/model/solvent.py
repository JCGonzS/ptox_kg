from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from .base import Base


class Solvent(Base):
    __tablename__ = "solvent"

    solvent_id = Column("solvent_id", Integer, primary_key=True)
    solvent_name = Column("solvent_name", String, nullable=False, unique=True)
    # One to Many (Solvent >>> Contrasts)
    contrast = relationship("Contrast", back_populates="solvent")

    __table_args__ = ()
