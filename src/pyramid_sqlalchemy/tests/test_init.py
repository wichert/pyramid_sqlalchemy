import unittest
from sqlalchemy import create_engine
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
        import mock

        class Registry:
            settings = {'sqlalchemy.url': 'sqlite://'}

        class Config:
            registry = Registry

        config = Config()
        with mock.patch('pyramid_sqlalchemy.init_sqlalchemy') as init_sqlalchemy:
            includeme(config)
            self.assertTrue(init_sqlalchemy.called)
            engine = init_sqlalchemy.mock_calls[0][1][0]
            self.assertEqual(str(engine.url), 'sqlite://')
