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


.. warning::

   It is critical that you call the setUp() method of the base classes first.
   This is necessary to guarantee everything is configured correctly before you
   run any code that might touch pyramid_sqlalchemy.

Writing functional tests is just as easy. The example below is a modified
version of the :ref:`Pyramid functional test example
<pyramid:functional_tests>`.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy.testing import DatabaseTestCase

   class FunctionalTests(DatabaseTestCase):
       def setUp(self):
           from myapp import main
           from webtest import TestApp
           super(FunctionalTests, self).setUp()
           app = main({})
           self.testapp = TestApp(App)



Normally all tests are run with an in-memory SQLite database. There are several
ways to change this:

* Set the ``db_uri`` variable in your test class to a different database URI.
* Set the ``DB_URI`` environment variable.
* If you use pytest as test runner you can use the ``--sql-url`` option to
  set the database URI.


py.test fixtures
----------------

If you use `pytest <http://pytest.org/>`_ you can use the test fixtures provided
by pyramid_sqlalchemy.

For tests that need an active connection, but that do not need to use SQLAlchemy
there is a ``transaction`` fixture available. This fixture creates a new transaction
that will automatically be aborted at the end of the test. In order to prevent the
transaction from being committed accidentally it is marked as `doomed`: this will
turn any call to ``commit()`` into an error.

.. code-block:: python
   :linenos:

   @pytest.mark.usefixtures('transaction')
   def test_transaction_integration():
       # Test code that needs a transaction

The ``sql_session`` fixture must be used to test any code that needs to access
a database. This fixture will setup a SQL backend and create all known tables.
To speed up tests this will only be done once for the py.test session. Each
test itself is running within its own transaction, to guarantee that any
database changes are reverted after the test, and the next test starts with a
clean database.

.. code-block:: python
   :linenos:

   def test_model_sets_id_automatically(sql_session):
       obj = Account(login='jane')
       sql_session.add(obj)
       sql_session.flush()
       assert obj.id is not None

Normally all tests will use an in-memory SQLite database. You can run your tests
with a different backend by using the ``--sql-url=<url>`` commandline option. For
example to run all tests against a local PostgreSQL server using the `pytest`
database::

    $ bin/py.test --sql-url=postgresql:///pytest

There is also a ``--sql-echo`` commandline option which will echo all executed SQL
statements to the console. This must be used in combination with pytests' ``-s``
option to make the console output visisble.

::

    $ bin/py.test --sql-echo -s
    ======================================= test session starts ========================================
    platform darwin -- Python 2.7.8 -- py-1.4.20 -- pytest-2.5.2
    plugins: pyramid-sqlalchemy
    collected 36 items / 3 skipped 

    tests/ext/test_sql.py 2014-08-30 09:02:38,070 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
    2014-08-30 09:02:38,070 INFO sqlalchemy.engine.base.Engine ()
    2014-08-30 09:02:38,070 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1

Using the provided fixtures you can create a new fixture for functional tests.
This fixture needs add a special key to the request environment to tell the
`pyramid_tm` tween not to to create or commit transactions.

.. code-block:: python
   :linenos:

   import pytest
   from webtest import TestApp
   from myapp import main

   @pytest.fixture
   def app(monkeypatch, sql_session):
       # Prevent SQL re-configuration with non-testing setup
       monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)
       app = main({})
       return TestApp(app, extra_environ={'repoze.tm.active': True})

