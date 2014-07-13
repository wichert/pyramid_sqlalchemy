Writing tests
=============

unittest test cases
-------------------

pyramid_sqlalchemy provides a ``DatabaseTestCase`` class which can be used when
writing unit or integration tests that require a working database. You can use
this as base class for you test classes. This example updates the
:ref:`Pyramid integration test example <pyramid:integration_tests>` to add
database support.


.. code-block:: python
   :linenos:


   from pyramid_sqlalchemy.testing import DatabaseTestCase
   from pyramid import testing

   class ViewIntegrationTests(DatabaseTestCase):
       def setUp(self):
           super(ViewIntegrationTests, self).setUp()
           self.config = testing.setUp()
           self.config.include('myapp')

       def tearDown(self):
           testing.tearDown()
           super(ViewIntegrationTests, self).tearDown()


When writing functional tests you need to make sure the application does not
try to initialise SQLAlchemy a second time. The easiest way to do is to mock
out the initialisation code. The example below is a modified version of the
:ref:`Pyramid functional test example <pyramid:functional_tests>`.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy.testing import DatabaseTestCase

   class FunctionalTests(unittest.TestCase):
       def setUp(self):
           from myapp import main
           from webtest import TestApp
           import mock
           super(ViewIntegrationTests, self).setUp()
           self._sql_patcher = mock.patch('pyramid_sqlalchemy.includeme')
           self._sql_patcher.start()
           app = main({})
           self.testapp = TestApp(App)

       def tearDown(self):
           self._sql_patcher.stop()
           super(ViewIntegrationTests, self).tearDown()


py.test fixtures
----------------

If you use `pytest <http://pytest.org/>`_ for your tests you will need define a
couple of fixtures to handle tests. First you need a SQLAlchemy-fixture which
sets up a database and its tables.

.. code-block:: python
   :linenos:

   import pytest
   from sqlalchemy import create_engine
   from pyramid_sqlalchemy import Session
   from pyramid_sqlalchemy import metadata

   def pytest_addoption(parser):
       parser.addoption('--sql-url', default='sqlite:///',
               help='SQLAlchemy Database URL')
       parser.addoption('--sql-echo', default=False, action='store_true',
               help='Echo SQL statements to console')

   def pytest_generate_tests(metafunc):
       if 'sqlalchemy_url' in metafunc.fixturenames:
           metafunc.parametrize('sqlalchemy_url', [metafunc.config.option.sql_url], scope='session')
       if 'sql_echo' in metafunc.fixturenames:
           metafunc.parametrize('sql_echo', [metafunc.config.option.sql_echo], scope='session')

   @pytest.yield_fixture(scope='session')
   def _sqlalchemy(sqlalchemy_url, sql_echo):
       engine = create_engine(sqlalchemy_url, echo=sql_echo)
       if engine.dialect.name == 'sqlite':
           engine.execute('PRAGMA foreign_keys = ON')
       # Check if a previous test has kept a session open. This will silently
       # make Session.configure do nothing and then break all our tests.
       assert not Session.registry.has()
       init_model(engine)
       metadata.create_all(engine)
   
       yield Session()
   
       Session.remove()
       metadata.drop_all(engine)
       Session.configure(bind=None)
       metadata.bind = None
       engine.dispose()

A session scope is used so the database is only created once. This fixture
also adds two commandline options to the test runner:

* ``--sql-echo`` will echo all executed SQL statements to the console
* ``--sql-url=<url>`` can be used to run the tests against a different database.


Next you need a fixture which creates a transaction for each test.

.. code-block:: python
   :linenos:

   import pytest
   import mock

   @pytest.yield_fixture
   def transaction():
       import transaction
       tx = transaction.begin()
       tx.doom()  # Make sure a transaction can never be commited.
       # Mock out transaction.get so code can call abort
       with mock.patch('transaction.get'):
           yield
       tx.abort()

We can now combine the previous two fixtures to create a ``sqlalchemy`` fixture
which provides a test with a working database in a transaction.

.. code-block:: python
   :linenos:

   import pytest

   @pytest.fixture
   def sqlalchemy(transaction, _sqlalchemy):
       return _sqlalchemy

Finally we can create a fixture for functional tests. This fixture needs to
mock out ``pyramid_sqlalchemy.includeme`` to prevent double initialisation of
SQLAlchemy, and it adds a magic key to the request environment so pyramid_tm
will not try to create or commit transactions.


.. code-block:: python
   :linenos:

   import pytest
   from webtest_plus import TestApp
   from myyapp import main

   @pytest.fixture
   def app(transaction, sqlalchemy, monkeypatch):
       # The sqlalchemy fixture already configured SQL for us, so make sure
       # it is not run again which would result in a second connection.
       monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)
       app = main({})
       return TestApp(app, extra_environ={'repoze.tm.active': True})
