try:
    from unittest import mock
except ImportError:
    import mock
import pytest
from sqlalchemy import create_engine
from .testing import DatabaseTestCase
from .meta import get_connection_info


DEFAULT_URI = 'sqlite:///'


def pytest_addoption(parser):
    parser.addoption('--sql-url', default=DEFAULT_URI,
                     help='SQLAlchemy Database URL')
    parser.addoption('--sql-echo', default=False, action='store_true',
                     help='Echo SQL statements to console')


def pytest_configure(config):
    DatabaseTestCase.db_uri = config.getoption('sql_url')


def sql_session_fixture(name, url, echo=False):
    engine = create_engine(url, echo=echo)

    if engine.dialect.name == 'sqlite':
        engine.execute('PRAGMA foreign_keys = ON')

    con_info = get_connection_info(name)
    # Check if a previous test has kept a session open. This will silently
    # make Session.configure do nothing and then break all our tests.
    assert not con_info.session_factory.registry.has()

    con_info.bind(engine)
    con_info.metadata.create_all(engine)

    yield con_info.session_factory()

    con_info.session_factory.remove()
    con_info.metadata.drop_all(engine)
    con_info.unbind()
    engine.dispose()


@pytest.yield_fixture(scope='session')
def _sqlalchemy(request):
    for f from sql_session_fixture('default',
                                   url=request.config.option.sql_url,
                                   echo=request.config.option.sql_echo):
        yield f


@pytest.yield_fixture
def transaction():
    """Create a new transaction for a test. The transaction is automatically
    marked as doomed to prevent it from being committed accidentily. At the end
    of the test it will be rolled back.
    """
    import transaction
    tx = transaction.begin()
    tx.doom()  # Make sure a transaction can never be commited.
    # Mock out transaction.commit so code can never commit around us.
    with mock.patch('transaction.Transaction.commit'):
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
    monkeypatch.setattr('pyramid_sqlalchemy.pyramid.includeme', lambda c: None)
    return _sqlalchemy


__all__ = ['transaction', 'sql_session']
