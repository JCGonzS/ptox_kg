import pandas as pd
import numpy as np

from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert

from .base import Base


# fmt: off
class RangeFinding(Base):
    __tablename__ = "range_finding"

    range_finding_id = Column("range_finding_id", Integer, primary_key=True)
    ptx_code = Column("ptx_code", Integer, ForeignKey("chemical.ptx_code"), nullable=False)
    biosystem_id = Column("biosystem_id", Integer, ForeignKey("biosystem.biosystem_id"), nullable=False)
    endpoint_id = Column("endpoint_id", Integer, ForeignKey("endpoint.endpoint_id"), nullable=False)
    experiment_id_auto = Column("experiment_id_auto", String, nullable=False)
    replicate = Column("replicate", Integer, nullable=False)
    number_animals_wells = Column("number_animals_wells", Float, nullable=False)
    vehicle = Column("vehicle", String, nullable=False)
    exposure_duration_h = Column("exposure_duration_h", Float, nullable=False)
    concentration_micromolar: float = Column("concentration_micromolar", Float, nullable=False)
    ptox_partner_id = Column("ptox_partner_id", String, nullable=False)
    source_file = Column("source_file", String, nullable=False)
    purpose = Column("purpose", String, nullable=True)
    effect = Column("effect", Float, nullable=True)
    variance_reduction = Column("variance_reduction", String, nullable=True)
    p_value_arithm = Column("p_value_arithm", Float, nullable=True)
    p_value_log = Column("p_value_log", Float, nullable=True)
    model_status = Column("model_status", String, nullable=True)
    user_flag = Column("user_flag", String, nullable=True)
    bmd10 = Column("bmd10", Float, nullable=True)
    bmd25 = Column("bmd25", Float, nullable=True)
    bmd50 = Column("bmd50", Float, nullable=True)
    slope = Column("slope", String, nullable=True)
    df = Column("df", Float, nullable=True)
    max = Column("max", Float, nullable=True)
    min = Column("min", Float, nullable=True)
    max_observed = Column("max_observed", Float, nullable=True)
    aic_delta = Column("aic_delta", Float, nullable=True)
    notes = Column("notes", String, nullable=True)

    # Many to One (Range-finding Experiment >>> Chemical)
    chemical = relationship("Chemical", back_populates="range_finding")
    # Many to One (Range-finding Experiment >>> Biosystem)
    biosystem = relationship("Biosystem", back_populates="range_finding")
    # Many to One (Range-finding Experiment >>> Endpoint)
    endpoint = relationship("Endpoint", back_populates="range_finding")

    # UniqueConstraint(
    #     experiment_id_auto,
    #     purpose,
    #     replicate,
    #     endpoint,
    #     number_animals_wells,
    #     vehicle,
    #     exposure_duration_h,
    #     concentration_micromolar,
    #     effect,
    #     variance_reduction,
    #     p_value_arithm,
    #     p_value_log,
    #     model_status,
    #     user_flag,
    #     bmd10,
    #     bmd25,
    #     bmd50,
    #     slope,
    #     df,
    #     max,
    #     min,
    #     max_observed,
    #     aic_delta,
    #     notes,
    #     name="uq_range_finding_row",
    # )


def insert_range_finding(session, rf_df):
    rf_df = rf_df.replace(np.nan, None)
    val_to_be_upsert = rf_df.to_dict("records")
    for val in val_to_be_upsert:
        insert_stmt = insert(RangeFinding).values(val)
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
            constraint="range_finding_uix_1"
        )
        session.execute(do_nothing_stmt)
    session.commit()
