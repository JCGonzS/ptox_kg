from sqlalchemy import Column, Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Timepoint(Base):
    __tablename__ = "timepoint"

    timepoint_id = Column("timepoint_id", Integer, primary_key=True)
    timepoint_code = Column("timepoint_code", String(5), nullable=False)
    timepoint_hr = Column("timepoint_hr", Integer, nullable=False)
    biosystem_id: int = Column("biosystem_id", Integer, ForeignKey("biosystem.biosystem_id"), nullable=False)
    # Many to One (Timepoints >>> Biosystem)
    biosystem = relationship("Biosystem", back_populates="timepoint")
    # One to Many (Timepoint >>> Contrasts)
    contrast = relationship("Contrast", back_populates="timepoint")

    __table_args__ = (
        UniqueConstraint(
            biosystem_id, timepoint_code, name="uq_timepoint_biosystem_id_timepoint_code"
        ),
        UniqueConstraint(
            biosystem_id, timepoint_hr, name="uq_timepoint_biosystem_id_timepoint_hr"
        ),
        Index("ix_timepoint_biosystem_id", biosystem_id),
    )
