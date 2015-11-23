try:
    from unittest import mock
except ImportError:
    import mock
import pytest
from sqlalchemy import create_engine
from .testing import DatabaseTestCase
from . import Session
from . import metadata
from . import init_sqlalchemy


DEFAULT_URI = 'sqlite:///'


def pytest_addoption(parser):
    parser.addoption('--sql-url', default=DEFAULT_URI,
            help='SQLAlchemy Database URL')
    parser.addoption('--sql-echo', default=False, action='store_true',
            help='Echo SQL statements to console')


def pytest_configure(config):
    DatabaseTestCase.db_uri = config.getoption('sql_url')


def pytest_generate_tests(metafunc):
    if 'sqlalchemy_url' in metafunc.fixturenames:
        metafunc.parametrize('sqlalchemy_url',
        [metafunc.config.getoption('sql_url')], scope='session')
    if 'sql_echo' in metafunc.fixturenames:
        metafunc.parametrize('sql_echo',
        [metafunc.config.getoption('sql_echo')], scope='session')


@pytest.yield_fixture(scope='session')
def _sqlalchemy(sqlalchemy_url, sql_echo):
    engine = create_engine(sqlalchemy_url, echo=sql_echo)
    if engine.dialect.name == 'sqlite':
        engine.execute('PRAGMA foreign_keys = ON')
    # Check if a previous test has kept a session open. This will silently
    # make Session.configure do nothing and then break all our tests.
    assert not Session.registry.has()
    init_sqlalchemy(engine)
    metadata.create_all(engine)

    yield Session()

    Session.remove()
    metadata.drop_all(engine)
    Session.configure(bind=None)
    metadata.bind = None
    engine.dispose()


@pytest.yield_fixture
def transaction():
    """Create a new transaction for a test. The transaction is automatically
    marked as doomed to prevent it from being committed accidentily. At the end
    of the test it will be rolled back.
    """
    import transaction
    tx = transaction.begin()
    tx.doom()  # Make sure a transaction can never be commited.
    # Mock out transaction.get so code can call abort
    with mock.patch('transaction.get'):
        yield
    tx.abort()


@pytest.fixture
def sql_session(transaction, _sqlalchemy, monkeypatch):
    """Provide a configured SQLAlchemy session running within a transaction.
    You can use the --sql-url commandline option to specify the SQL backend to
    use. The default configuration will use an in-memory SQLite database.

    You can also use the --sql-echo option to enable logging of all SQL
    statements to the console.
    """
    # SQL is already configured, so make sure it is not run again which would
    # result in a second connection.
    monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)
    return _sqlalchemy


__all__ = ['transaction', 'sql_session']
