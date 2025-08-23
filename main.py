import os
import yaml
import pickle
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.build_graph import build_graph_from_db


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

graph_name = "ptox_kg"
graphml_file = f"{graph_name}.graphml"
pkl_file = f"{graph_name}.pkl"

# Setup DB session
engine = connect_to_database(config)
Session = sessionmaker(bind=engine)
session = Session()

# Build graph if it does not exist
if os.path.isfile(pkl_file):
    G = pickle.load(open(pkl_file, "rb"))
else:
    G = build_graph_from_db(session, graph_name)

print(G.number_of_nodes())
print(G.number_of_edges())
