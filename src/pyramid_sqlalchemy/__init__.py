from .meta import (
    get_connection_info,
    get_metadata,
    get_sql_session,
    BaseObject,
    Session,
    metadata,
)
from .pyramid import includeme  # noqa


def bind_connection(engine, name='default'):
    """Bind a named connection to a SQLAlchemy engine.

    This must be called before using using any of the SQLAlchemy managed
    tables or classes linked to the connection.
    """
    get_connection_info(name).bind(engine)


def init_sqlalchemy(engine):
    """Initialise the SQLAlchemy connection.

    This must be called before using using any of the SQLAlchemy managed
    tables or classes in the model.

    This will only configure the default connection. If you want to
    """
    bind_connection(engine)


__all__ = [
    'get_connection_info', 'get_metadata', 'get_sql_session',
    'BaseObject', 'Session', 'metadata'
]
