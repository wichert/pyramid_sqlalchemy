import unittest
from sqlalchemy import create_engine
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import metadata
from pyramid_sqlalchemy import Session
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
            metadata.create_all()
        super(DatabaseTestCase, self).setUp()

    def tearDown(self):
        transaction.abort()
        Session.remove()
        if self.create_tables:
            metadata.drop_all()
        Session.configure(bind=None)
        metadata.bind = None
        self.engine.dispose()
        super(DatabaseTestCase, self).tearDown()
