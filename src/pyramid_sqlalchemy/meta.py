from types import ModuleType
from sqlalchemy import event, orm, schema
from sqlalchemy.ext.declarative import declarative_base
import zope.sqlalchemy
import pyramid_sqlalchemy.model


_KEY_DATA = {}


class ConnectionInfo:
    def __init__(self, name, session_factory=None):
        self.name = name
        self.metadata = schema.MetaData(info={'connection_name': name})
        self.orm_base = declarative_base(metadata=self.metadata)
        # TODO This should be configurable
        self.session_factory = session_factory or \
            orm.scoped_session(orm.sessionmaker())
        _setup_session_factory(name, self.session_factory, self.orm_base)

    def bind(self, engine):
        self.session_factory.configure(bind=engine)
        self.metadata.bind = engine

    def configure(self, **kw):
        self.session_factory.configure(**kw)

    def unbind(self):
        self.session_factory.configure(bind=None)
        self.metadata.bind = None


def _setup_session_factory(name, session_factory, orm_base):
    zope.sqlalchemy.register(session_factory)

    if name == 'default':
        module = pyramid_sqlalchemy.model
    else:
        module = ModuleType('pyramid_sqlalchemy.model.%s' % name)
        module.__package__ = pyramid_sqlalchemy.model
        setattr(pyramid_sqlalchemy.model, name, module)

    event.listen(orm_base, 'class_instrument',
                 lambda cls: setattr(module, cls.__name__, cls))
    event.listen(orm_base, 'class_uninstrument',
                 lambda cls:
                 hasattr(module, cls.__name__) and
                 delattr(module, cls.__name__))


def get_connection_info(name='default'):
    data = _KEY_DATA.get(name)
    if not data:
        _KEY_DATA[name] = data = ConnectionInfo(name)
    return data


def configure_all_connections(**kw):
    for v in _KEY_DATA.values():
        v.configure(**kw)


def orm_base(name='default'):
    return get_connection_info(name).orm_base


def get_metadata(name='default'):
    return get_connection_info(name).metadata


def get_sql_session(name='default'):
    return get_connection_info(name).session_factory


def get_sql_query(cls):
    con_info = cls.__table__.info['connection_name']
    return con_info.session_factory().query(cls)


#: Global metadata, bound to the `default` connection.
metadata = get_metadata()

#: Base class for the SQLAlchemy ORM. This will be bound to the `default`
#: connection.
BaseObject = orm_base()

#: Global session factory for the `default` connection.
Session = get_sql_session()


__all__ = ['Session', 'metadata', 'BaseObject']
