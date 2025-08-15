from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship


from .base import Base


class File(Base):
    __tablename__ = "file"

    # Primary key column
    file_id: int = Column("file_id", Integer, primary_key=True)
    # Non nullable columns
    file_name: str = Column("file_name", String, nullable=False)
    time_last_mod = Column("time_last_mod", DateTime(timezone=True), nullable=False)
    rows_total: int = Column("rows_total", Integer, nullable=False)
    rows_inserted: int = Column("rows_inserted", Integer, nullable=False)
    time_insertion = Column(
        "time_insertion",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    db_table: str = Column("db_table", String, nullable=False)
    # Nullable columns
    missing_sheets: str = Column("missing_sheets", String, nullable=True)
    missing_columns: str = Column("missing_columns", String, nullable=True)
    missing_values: str = Column("missing_values", String, nullable=True)
    wrong_dtype_columns: str = Column("wrong_dtype_columns", String, nullable=True)

    # rnaseq_contrast_pilot: relationship = relationship("ContrastPilot", back_populates="file")

    # Constraints
    UniqueConstraint(file_name, db_table, name="file_name_table_uix_1")


def insert_file(session, file_dict, mode="insert"):
    for key in file_dict:
        if isinstance(file_dict[key], list):
            if len(file_dict[key]) > 0:
                file_dict[key] = ",".join(file_dict[key])
            else:
                file_dict[key] = None

    updateable_fields = [
        "rows_total",
        "rows_inserted",
        "missing_sheets",
        "missing_columns",
        "missing_values",
        "wrong_dtype_columns",
    ]
    insert_stmt = insert(File).values(file_dict)
    if mode == "insert":
        do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
            constraint="file_name_table_uix_1"
        )
        session.execute(do_nothing_stmt)
    elif mode == "upsert":
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint="file_name_table_uix_1",
            set_={field: insert_stmt.excluded[field] for field in updateable_fields}
        )
        session.execute(do_update_stmt)
    session.commit()
    return
