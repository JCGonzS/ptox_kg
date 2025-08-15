from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from .base import Base


class ColumnDescription(Base):
    __tablename__ = "column_description"

    column_id: int = Column("column_id", Integer, primary_key=True, autoincrement=True)
    column_name: str = Column("column_name", String, nullable=False)
    table_name: str = Column("table_name", String, nullable=False)
    column_desc: str = Column("column_description", String, nullable=False)
