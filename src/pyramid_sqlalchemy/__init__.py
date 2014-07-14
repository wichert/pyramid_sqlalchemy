import logging
from sqlalchemy import engine_from_config
from sqlalchemy.engine.interfaces import Dialect
from pyramid_sqlalchemy.meta import metadata
from pyramid_sqlalchemy.meta import BaseObject
from pyramid_sqlalchemy.meta import Session
import pyramid_sqlalchemy.events
pyramid_sqlalchemy.events  # Keep PyFlakes happy


log = logging.getLogger('pyramid_sqlalchemy')


def init_sqlalchemy(engine):
    """Initialise the SQLAlchemy models. This must be called before using
    using any of the SQLAlchemy managed the tables or classes in the model."""
    if engine.dialect.__class__.do_begin_twophase is Dialect.do_begin_twophase:
        Session.configure(twophase=False)
        log.warn('SQL dialect %s does not support two-phase commits',
                engine.dialect.name)
    else:
        log.debug('Enabling two-phase commit support.')
        Session.configure(twophase=True)
    Session.configure(bind=engine)
    metadata.bind = engine


def includeme(config):
    """'Convenience method to initialise all components of this
    :mod:`pyramid_sqlalchemy` package from a pyramid applicaiton.
    """
    engine = engine_from_config(config.registry.settings, 'sqlalchemy.')
    init_sqlalchemy(engine)


__all__ = ['BaseObject', 'Session', 'metadata', 'init_model']
