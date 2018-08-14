try:
    from unittest import mock
except ImportError:
    import mock
from pyramid.config import Configurator


def test_two_phase_directive():
    config = Configurator()
    with mock.patch('pyramid_sqlalchemy.meta.ConnectionInfo.configure') \
            as configure:
        with mock.patch('pyramid_sqlalchemy.meta.ConnectionInfo.bind'):
            config.include('pyramid_sqlalchemy')
            config.enable_sql_two_phase_commit()
    configure.assert_called_with(twophase=True)
