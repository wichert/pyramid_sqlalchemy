import unittest
from sqlalchemy import create_engine
from pyramid.config import Configurator
from pyramid_sqlalchemy import includeme
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import Session


class test_init_sqlalchemy(unittest.TestCase):
    def test_basic_sqlite(self):
        engine = create_engine('sqlite://')
        init_sqlalchemy(engine)
        self.assertTrue(Session.session_factory.kw['bind'] is engine)


class includeme_tests(unittest.TestCase):
    def test_sqlite_config(self):
        try:
            from unittest import mock
        except ImportError:
            import mock

        config = Configurator(settings={'sqlalchemy.url': 'sqlite://'})

        with mock.patch('pyramid_sqlalchemy.init_sqlalchemy') as init_sqlalchemy:
            includeme(config)
            self.assertTrue(init_sqlalchemy.called)
            engine = init_sqlalchemy.mock_calls[0][1][0]
            self.assertEqual(str(engine.url), 'sqlite://')

    def test_two_phase_directive(self):
        try:
            from unittest import mock
        except ImportError:
            import mock

        config = Configurator()
        with mock.patch('pyramid_sqlalchemy.Session.configure') as configure:
            with mock.patch('pyramid_sqlalchemy.engine_from_config'):
                with mock.patch('pyramid_sqlalchemy.init_sqlalchemy'):
                    config.include('pyramid_sqlalchemy')
                    config.enable_sql_two_phase_commit()
        configure.assert_called_with(twophase=True)
