import argparse
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session
from marc_honest.models import Base


def get_marc_honest_url() -> str:
    try:
        os.environ["MARC_HONEST_URL"]
    except KeyError:
        #print("MARC_HONEST_URL environment variable not set, using in-memory db")
        return "sqlite:///:memory:"
    return os.environ["MARC_HONEST_URL"]


def create_database(database_url: str = get_marc_honest_url()):
    """
    Create the database tables that don't exist using the provided database URL.

    Parameters:
    database_url (str): The database URL.
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(engine, checkfirst=True)


def get_connection(database_url: str = get_marc_honest_url()) -> Connection:
    """
    Get a connection to the database using the provided database URL.

    Parameters:
    database_url (str): The database URL.

    Returns:
    connection: The connection to the database.
    """
    engine = create_engine(database_url)
    connection = engine.connect()
    return connection


def get_session(database_url: str = get_marc_honest_url()) -> Session:
    """
    Get a session to the database using the provided database URL.

    Parameters:
    database_url (str): The database URL.

    Returns:
    session: The session to the database.
    """
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def init(argv: list[str]):
    parser = argparse.ArgumentParser(description="Initialize the database.")
    parser.add_argument("--db_url", default=get_marc_honest_url(), help="The database URL.")
    args = parser.parse_args(argv)

    create_database(args.db_url)
    print(f"Database initialized at {args.db_url}")