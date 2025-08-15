from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class ChemicalAssociation(Base):
    __tablename__ = "chemical_association"

    association_id = Column("association_id", Integer, primary_key=True)
    ptx_code = Column("ptx_code", Integer, ForeignKey("chemical.ptx_code"), nullable=False)
    term = Column("term", String, nullable=False)
    external_id = Column("external_id", String, nullable=True)
    association_type = Column("association_type", String, nullable=False)
    socio_affinity_score = Column("socio_affinity_score", Float, nullable=False)
    pubmed_count = Column("pubmed_count", Integer, nullable=False)
    pubmed_ids = Column("pubmed_ids", String, nullable=False)
    z_score = Column("z_score", Float, nullable=False)
    # Many to One (Chem. Association >> Chemical)
    chemical = relationship("Chemical", back_populates="association")

    __table_args__ = (
        Index("ix_chemical_association_ptx_code", ptx_code),
        UniqueConstraint(ptx_code, term, name="uq_chemical_association_ptx_code_term"),
    )
    