import os
import yaml
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sql.extract import fetch_chemicals, fetch_organisms, fetch_biosystems, fetch_proteins
from src.transform import build_nodes_and_edges


def connect_to_database(config):
    connection_url = (
        "postgresql://"
        + str(config["psql_user"])
        + ":"
        + str(config["psql_pass"])
        + "@"
        + str(config["psql_host"])
        + ":"
        + "5432"
        + "/"
        + str(config["psql_db_name"])
    )
    engine = create_engine(connection_url, echo=False)
    return engine


# Load database connection parameters from .yaml file
HERE_PATH = os.path.dirname(os.path.abspath(__file__))
with open(f"{HERE_PATH}/config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# Setup DB session
engine = connect_to_database(config)
Session = sessionmaker(bind=engine)
session = Session()

# 1. Extract
chemicals = fetch_chemicals(session)
organisms = fetch_organisms(session)
biosystems = fetch_biosystems(session)
proteins = fetch_proteins(session)

# 2. Transform to nodes & edges
nodes, edges = build_nodes_and_edges(
    chemicals, 
    organisms, 
    biosystems,
    proteins
)

for node in nodes:
    print(node)

for edge in edges:
    print(edge)