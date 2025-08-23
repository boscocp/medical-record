import os
import MySQLdb
import MySQLdb.connections
import MySQLdb.converters

from sqlalchemy import Engine, create_engine

DB_MAX_OVERFLOW = 0
DB_POOL_SIZE = 1
DB_POOL_RECYCLE = 3_600
DB_DEBUG_MODE = True
db_conn_string = os.getenv(
    "DATABASE_URL", "mysql://localadmin:localadmin@database:3306/medical_record")

_engine = create_engine(
    db_conn_string,
    echo=DB_DEBUG_MODE,
    pool_size=DB_POOL_SIZE,
    pool_recycle=DB_POOL_RECYCLE,
    pool_pre_ping=True,
    pool_use_lifo=True,
)


def create_db_engine() -> Engine:
    """ It creates sqlalchemy engine instance.
    Returns
    -------
    Engine
        SQLAlchemy engine instance
    """
    return _engine
