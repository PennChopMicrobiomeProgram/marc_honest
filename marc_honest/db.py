import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, Session
from marc_honest.models import Base, Specimen, Subject


def get_marc_honest_url() -> str:
    return os.environ.get("MARC_HONEST_URL", "sqlite:///:memory:")


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

    # Test session by executing a simple query
    try:
        session.query(Subject).first()
        session.query(Specimen).first()
    except Exception as e:
        raise RuntimeError(
            "\nmarc_honest failed to connect to database: \n```"
            + str(e)
            + f"\n```\nDid you remember to set MARC_HONEST_URL: {os.environ.get('MARC_HONEST_URL')}?"
        )

    return session
