"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import register

#: SQLAlchemy session manager.  Updated by
# :py:func:`pyramid_sqlalchemy.init_sqlalchemy`.
Session = orm.scoped_session(orm.sessionmaker())
register(Session)

#: Proper naming convention for metadata as per 
#: alembic/sqlalchemy documentation
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

#: Global metadata. If you have multiple databases with overlapping table
#: names, you'll need a metadata for each database
metadata = schema.MetaData(naming_convention=NAMING_CONVENTION)

#: Base classes for models using declarative syntax
BaseObject = declarative_base(metadata=metadata)

__all__ = ['Session', 'metadata', 'BaseObject']
