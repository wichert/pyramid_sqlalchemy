try:
    from unittest import mock
except ImportError:
    import mock
import os
import unittest
from sqlalchemy import create_engine
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import metadata
from pyramid_sqlalchemy import Session
import transaction


class DatabaseTestCase(unittest.TestCase):
    """Base class for tests which require a database connection.

    This class provides makes sure a SQL connection to a database is available
    for tests. Each test is run in a separate transaction, and all tables are
    recreated for each test to guarantee a clean slate.
    """

    #: FLag indicating if SQL tables should be created. This is normally
    #: set to `True`, but you may want to disabled table creation when writing
    #: tests for migration code.
    create_tables = True

    #: :ref:`Database URL <sqlalchemy:database_urls>` for the test database.
    #: Normally a private in-memory SQLite database is used. You can override
    #: this with the pytest --sql-url parameter, or the DB_URI environment
    #: environment variable.
    db_uri = 'sqlite://'

    def database_url(self):
        return os.environ.get('DB_URI', self.db_uri)

    def setUp(self):
        self.engine = create_engine(self.database_url())
        if self.engine.dialect.name == 'sqlite':
            self.engine.execute('PRAGMA foreign_keys = ON')
        init_sqlalchemy(self.engine)
        if self.create_tables:
            metadata.create_all()
        super(DatabaseTestCase, self).setUp()
        self._sqlalchemy_patcher = mock.patch('pyramid_sqlalchemy.includeme', lambda c: None)
        self._sqlalchemy_patcher.start()

    def tearDown(self):
        transaction.abort()
        Session.remove()
        if self.create_tables:
            metadata.drop_all()
        Session.configure(bind=None)
        metadata.bind = None
        self.engine.dispose()
        self._sqlalchemy_patcher.stop()
        super(DatabaseTestCase, self).tearDown()


__all__ = ['DatabaseTestCase']
