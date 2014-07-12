import unittest


class test_init_sqlalchemy(unittest.TestCase):
    def init_sqlalchemy(self, *a, **kw):
        from pyramid_sqlalchemy import init_sqlalchemy
        return init_sqlalchemy(*a, **kw)

    def test_basic_sqlite(self):
        from sqlalchemy import create_engine
        from pyramid_sqlalchemy import meta
        engine = create_engine('sqlite://')
        self.init_sqlalchemy(engine)
        self.assertTrue(meta.Session.session_factory.kw['bind'] is engine)


class includeme_tests(unittest.TestCase):
    def includeme(self, *a, **kw):
        from pyramid_sqlalchemy import includeme
        return includeme(*a, **kw)

    def test_sqlite_config(self):
        import mock
        from pyramid_sqlalchemy import meta

        class Registry:
            settings = {'sqlalchemy.url': 'sqlite://'}

        class Config:
            registry = Registry

        config = Config()
        with mock.patch('pyramid_sqlalchemy.init_sqlalchemy') as init_sqlalchemy:
            self.includeme(config)
            self.assertTrue(init_sqlalchemy.called)
            engine = init_sqlalchemy.mock_calls[0][1][0]
            self.assertEqual(str(engine.url), 'sqlite://')
