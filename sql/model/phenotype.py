import json

from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    Float,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

from .base import Base


class Phenotype(Base):
    __tablename__ = "phenotype"

    # Primary key column
    phenotype_id: int = Column("phenotype_id", Integer, primary_key=True)
    # Non-nullable columns
    experiment_id: str = Column(
        "experiment_id_auto", String, nullable=False, index=True
    )
    project_partner: str = Column("project_partner", String, nullable=False, index=True)
    strain: str = Column("strain", String, nullable=False)
    date_start: str = Column("date_start", String, nullable=False)
    start_exposure_stage: str = Column("start_exposure_stage", String, nullable=False)
    exposure_duration_h: float = Column("exposure_duration_h", Float, nullable=False)
    stage_effect_measurement: str = Column(
        "stage_effect_measurement", String, nullable=False
    )
    replicate: int = Column("replicate", Integer, nullable=False)
    exposure_concentration_nominal: float = Column(
        "exposure_concentration_nominal", Float, nullable=False
    )
    exposure_concentration_unit: str = Column(
        "exposure_concentration_unit", String(10), nullable=False
    )
    effect_type: str = Column("effect_type", String, nullable=False)
    effect_result: json = Column("effect_result", JSON, nullable=False)
    effect_unit: json = Column("effect_unit", JSON, nullable=False)
    # Nullable columns
    generation: str = Column("generation", String, nullable=True)
    buffer: str = Column("buffer", String, nullable=True)
    buffer_concentration: str = Column("buffer_concentration", String, nullable=True)
    buffer_concentration_unit: str = Column(
        "buffer_concentration_unit", String(10), nullable=True
    )
    vehicle: str = Column("vehicle", String, nullable=True)
    vehicle_percent: float = Column("vehicle_percent", Float, nullable=True)
    ph_start: float = Column(
        "ph_start", String, nullable=True
    )  # should be float but ranges found in some rows (e.g. 7.3-7.5)
    ph_end: float = Column("ph_end", String, nullable=True)
    number_specimen_total: int = Column("number_specimen_total", Integer, nullable=True)
    number_specimen_analysed: int = Column(
        "number_specimen_analysed", Integer, nullable=True
    )
    short_assay_description: str = Column(
        "short_assay_description", String, nullable=True
    )
    notes: str = Column("notes", String, nullable=True)

    # Many to One (Phenotype Experiments >>> Biosystem)
    biosystem_id: int = Column(
        "biosystem_id", Integer, ForeignKey("biosystem.biosystem_id"), nullable=False
    )
    biosystem = relationship("Biosystem", back_populates="phenotype_experiment")
    # Relationships many-to-one
    file_id: int = Column(Integer, ForeignKey("file.file_id"), nullable=False)
    file: relationship = relationship("File", backref="phenotype")
    ptx_code: int = Column("ptx_code", Integer, ForeignKey("chemical.ptx_code"), nullable=False)
    chemical: relationship = relationship("Chemical", backref="phenotype")


    # Constraints
    ### Commented out because can't be used with JSON columns
    UniqueConstraint(
        experiment_id,
        project_partner,
        strain,
        generation,
        date_start,
        buffer,
        buffer_concentration,
        buffer_concentration_unit,
        vehicle,
        vehicle_percent,
        ph_start,
        ph_end,
        number_specimen_total,
        number_specimen_analysed,
        start_exposure_stage,
        exposure_duration_h,
        stage_effect_measurement,
        replicate,
        exposure_concentration_nominal,
        exposure_concentration_unit,
        effect_type,
        short_assay_description,
        notes,
        file_id,
        name="phenotype_uix_1",
    )


def insert_phenotype(session, df, mode="insert"):
    inserted = 0
    not_inserted = 0
    list_of_dicts = df.to_dict("records")

    for dic in list_of_dicts:
        try:
            with session.begin_nested():
                insert_stmt = insert(Phenotype).values(dic)
                if mode == "insert":
                    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                        constraint="phenotype_uix_1"
                    )
                    session.execute(do_nothing_stmt)
                elif mode == "upsert":
                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        constraint="phenotype_uix_1", set_=insert_stmt.excluded
                    )
                    session.execute(do_update_stmt)
                inserted += 1

        except SQLAlchemyError as e:
            # print(e) # log somewhere
            not_inserted += 1

    session.commit()
    return inserted, not_inserted
