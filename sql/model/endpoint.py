from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .base import Base


class Endpoint(Base):
    __tablename__ = "endpoint"

    endpoint_id = Column("endpoint_id", Integer, primary_key=True)
    endpoint_code = Column("endpoint_code", String, nullable=False, unique=True)
    endpoint_description = Column("endpoint_description", String, nullable=False)

    # One to Many (Endpoint >>> Range-finding Experiment)
    range_finding = relationship("RangeFinding", back_populates="endpoint")