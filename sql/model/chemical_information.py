import re
import pandas as pd
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from .base import Base


class ChemicalInformation(Base):
    __tablename__ = "chemical_information"

    ptx_code = Column("ptx_code", Integer, ForeignKey("chemical.ptx_code"), primary_key=True)
    full_ptx_code = Column("full_ptx_code", String, nullable=False, unique=True)
    pubchem_cid = Column("pubchem_cid", Integer, nullable=False, unique=True)
    compound_name_user = Column("compound_name_user", String)
    # Rest of columns are added dynamically using 'add_chemical_properties()'
    # One to One (Chemical Information< > Chemical)
    chemical = relationship("Chemical", back_populates="information")

    __table_args__ = (
            Index("ix_chemical_information_full_ptx_code", full_ptx_code),
    )


def add_chemical_properties(update=False) -> list:
    """
    Add additional chemical properties as attributes (columns) to the
    'chemical_information' table. This info is stored in a CSV file
    
    Parameters:
        update: whether to regenerate the file with columns and their data types
    
    Return:
        list of properties added to the table
    """
    from ptoxdb.config import get_data_paths
    from ptoxdb.utils import export_sql_dtypes_to_csv

    dtype_map = {
        "Integer": Integer,
        "String": String,
        "Float": Float
    }
    data_paths = get_data_paths()

    if update:
        df = pd.read_csv(data_paths["chemical_annotations_ufz"])
        df.columns = df.columns.str.lower()
        replacements = [
            ("\\(", ""),
            ("\\)", ""),
            ("\\=", ""),
            ("[,;]", ""),
            ("\\]", ""),
            ("\\]", ""),
            ("[/]", " per "),
            ("[?]", ""),
            ("[µ]", "u"),
            (" ", ""),
            ("[ü]", "u"),
            ("[\r\n\t]", ""),
            ("[.]", "_"),
            ("[-]", "_"),
        ]
        for pat, repl in replacements:
            df.columns = [re.sub(pat, repl, x) for x in df.columns]
        schema_df = export_sql_dtypes_to_csv(df, data_paths["chemical_annotations_ufz_dtypes"])
    else:
        schema_df = pd.read_csv(data_paths["chemical_annotations_ufz_dtypes"])
    
    attributes = []
    for _, row in schema_df.iterrows():
        colname = row["column_name"]
        sql_dtype_str = row["sql_dtype"]
        sql_dtype = dtype_map.get(sql_dtype_str)

        if sql_dtype and colname not in dir(ChemicalInformation):
            attr_val = Column(sql_dtype, nullable=True)
            setattr(ChemicalInformation, colname, attr_val)
            attributes.append(colname)

    return attributes
