from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connect_to_psql_database(config):
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
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
