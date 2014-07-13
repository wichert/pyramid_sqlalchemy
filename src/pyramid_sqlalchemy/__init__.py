from sqlalchemy import engine_from_config
from pyramid_sqlalchemy.meta import metadata
from pyramid_sqlalchemy.meta import BaseObject
from pyramid_sqlalchemy.meta import Session
import pyramid_sqlalchemy.events
pyramid_sqlalchemy.events  # Keep PyFlakes happy


def init_sqlalchemy(engine):
    """Initialise the SQLAlchemy models. This must be called before using
    using any of the SQLAlchemy managed the tables or classes in the model."""
    Session.configure(bind=engine)
    metadata.bind = engine


def includeme(config):
    """'Convenience method to initialise all components of this
    :mod:`pyramid_sqlalchemy` package from a pyramid applicaiton.
    """
    engine = engine_from_config(config.registry.settings, 'sqlalchemy.')
    init_sqlalchemy(engine)


__all__ = ['BaseObject', 'Session', 'metadata', 'init_model']
