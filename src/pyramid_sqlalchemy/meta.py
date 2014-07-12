"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

#: SQLAlchemy session manager.  Updated by
# :py:func:`s4u.sqlalchemy.init_sqlalchemy`.
Session = orm.scoped_session(
        orm.sessionmaker(extension=ZopeTransactionExtension()))

#: Global metadata. If you have multiple databases with overlapping table
#: names, you'll need a metadata for each database
metadata = schema.MetaData()

#: Base classes for models using declarative syntax
BaseObject = declarative_base(metadata=metadata)

__all__ = ['Session', 'metadata', 'BaseObject']
