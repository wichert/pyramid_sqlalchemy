import unittest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import meta
import transaction


class DatabaseTestCase(unittest.TestCase):
    """Base class for tests which require a database.
    """
    create_tables = True
    db_uri = 'sqlite://'

    def setUp(self):
        self.engine = create_engine(self.db_uri)
        init_sqlalchemy(self.engine)
        if self.create_tables:
            meta.metadata.create_all()
        super(DatabaseTestCase, self).setUp()

    def tearDown(self):
        transaction.abort()
        meta.Session.remove()
        if self.create_tables:
            meta.metadata.drop_all()
        meta.Session.configure(bind=None)
        meta.metadata.bind = None
        self.engine.dispose()
        super(DatabaseTestCase, self).tearDown()


class RoundTripTestCase(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        cls.engine = create_engine('sqlite:///', echo=True)
        cls.metadata = MetaData(bind=cls.engine)
        cls.BaseObject = declarative_base(metadata=cls.metadata)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.metadata.create_all()
        self.session = self.Session()

    def tearDown(self):
        self.metadata.drop_all()

    @classmethod
    def teardownClass(cls):
        cls.Session.close_all()
        cls.engine.dispose()
