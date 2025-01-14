from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def get_remote_session():
    """
    Creates a SQLAlchemy session for the remote database.
    Assumes the remote database is configured under the key 'static_db'.
    """
    if 'static_db' not in db.engines:
        raise KeyError("The remote database engine 'static_db' is not configured in SQLAlchemy.")

    remote_engine = db.engines['static_db']
    Session = sessionmaker(bind=remote_engine)
    return Session()
