from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Index,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from .base import Base
from .organism import Organism


class Metabolite(Base):
    __tablename__ = "metabolite"

    metabolite_id = Column("metabolite_id", Integer, primary_key=True)
    metabolite_string_id = Column("metabolite_string_id", String, nullable=False)
    compound = Column("compound", String, nullable=True)
    ion = Column("ion", String, nullable=True)
    formula = Column("formula", String, nullable=True)
    inchikey = Column("inchikey", String, nullable=True)
    cid = Column("cid", Integer, nullable=True)
    kegg_id = Column("kegg_id", String, nullable=True)
    hmdb_id = Column("hmdb_id", String, nullable=True)
    in_mtox700 = Column("in_mtox700", String, nullable=True)
    rt = Column("rt", Float, nullable=True)
    mz = Column("mz", Float, nullable=True)
    charge = Column("charge", Integer, nullable=True)
    biosystem_id = Column( "biosystem_id", Integer, ForeignKey("biosystem.biosystem_id"), nullable=False)
    assay_id = Column("assay_id", Integer, ForeignKey("metabolomics_assay.assay_id"), nullable=False)

    # Many to One (Metabolites >>> Biosystem)
    biosystem = relationship("Biosystem", back_populates="metabolite")
    # Many to One (Metabolites >>> Assay)
    assay = relationship("MetabolomicsAssay", back_populates="metabolite")

    __table_args__ = (
        # cannot set this for now because the same metabolite_id for the same org does indeed have different annotations
        # PrimaryKeyConstraint(
        #     "metabolite_id", "ptox_biosystem_id", name="pk_metabolite"
        # ),
        UniqueConstraint(
            "metabolite_id",
            "compound",
            "ion",
            "formula",
            "inchikey",
            "cid",
            "kegg_id",
            "hmdb_id",
            "in_mtox700",
            "rt",
            "mz",
            "charge",
            "assay_id",
            "biosystem_id",
            name="ux_metabolite_row",
        ),
        Index("ix_metabolite_metabolite_id", "metabolite_id"),
        Index(
            "ix_metabolite_metabolite_id_biosystem_id",
            "metabolite_id",
            "biosystem_id",
        ),
        Index("ix_metabolite_compound", "compound"),
    )
