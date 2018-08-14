import re
from sqlalchemy import engine_from_config
from .meta import (
    configure_all_connections,
    get_connection_info,
    get_sql_query,
    get_sql_session,
)


def enable_sql_two_phase_commit(config):
    """Enable two-phase commit for all connections."""
    configure_all_connections(twophase=True)


def _find_config_prefixes(settings):
    for k in settings:
        m = re.match(r'^(sqlalchemy(\.[^.]+)).url', k)
        if m:
            yield m.gropus(1)


def includeme(config):
    """'Convenience method to initialise all components of this
    :mod:`pyramid_sqlalchemy` package from a pyramid applicaiton.
    """
    config.add_directive(name='enable_sql_two_phase_commit',
                         directive=enable_sql_two_phase_commit)
    config.add_request_method(name='sql_session',
                              callable=get_sql_session,
                              reify=True)
    config.add_request_method(name='sql_query', callable=get_sql_query)
    settings = config.get_settings()
    for (name, prefix) in _find_config_prefixes(settings):
        engine = engine_from_config(settings, prefix)
        get_connection_info(name).bind(engine)


__all__ = ['includeme']
