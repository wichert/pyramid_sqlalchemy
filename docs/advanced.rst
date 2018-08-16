Advanced topics
===============

Multiple databases
------------------

Sometimes you may need to talk to multiple databases. This requires you to do two
things: define the data model for each database, and configure the connection for
each database. pyramid_sqlalchemy has support for multiple databases build-in.

The first thing you will need to do is specify for each ORM class or table which
connection it is associated with. Each connection is identified by a name. If
you do not specify a name ``default`` is used instead.

.. caution::

   It is strongly recommended to enable two-phased transactions when using multiple
   databases. Without this there is a risk that the databases can be out of sync.

Here is an example that defines a `user` table in the default database, and a
`transaction` table in a data warehouse:


.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import orm_base

   class User(orm_base()):
       __tablename__ = 'user'


   class Transaction(orm_base('warehouse')):
       __tablename__ = 'transaction'


You can now see why ``orm_base`` is a function: you can pass it the connection name
and it will do the necessary linking.

The same approach works if you want to use the metadata instance directly, without
using the ORM:

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_metadata
   from sqlalchemy import Column, Table, Integer, String

   transaction = Table('transaction', get_metadata('warehouse),
       Column('tx_id', Integer, primary_key=True),
       ...
   )

To connect to a database you must call ``bind_connection`` once for each connection:

.. code-block:: python
   :linenos:

   from sqlalchemy import create_engine
   from pyramid_sqlalchemy import bind_connection

   # Use a local PostgreSQL database for each default data
   bind_connection(create_engine('postgresql:///myapp'))
   # And connect to a remote instance for our data warehouse
   bind_connection(create_engine('postgresql://data-warehouse/myapp'), 'warehouse')


When querying or updating a database you can request a session for a specific
connection. Building on our example, this is how you can retrieve the latest
transaction from the data warehouse:

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_sql_session

   sql_session = get_sql_session('warehouse')
   latest_tx = sql_session.query(Transaction)\
       .order_by(Transaction.timestamp)\
       .limit(1)\
       .first()

Since it can be tedious to always pass the name of the connection to
``get_sql_session`` you can also use ``get_sql_query``, which is smart
enough to figure out which session it needs to use.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_sql_query

   latest_tx = get_sql_query(Transaction)\
       .order_by(Transaction.timestamp)\
       .limit(1)\
       .first()


When writing tests you will need to define an extra fixture for extra
connections you create. This is easily done via the
:py:func:`pyramid_sqlalchemy.fixtures.sql_session_fixture`
helper.

.. code-block:: python
   :linenos:

   import pytest
   from pyramid_sqlalchemy.fixtures import sql_session_fixture

   @pytest.yield_fixture
   def warehouse_sql_session():
       """A SQLAlchemy session for the warehouse database.
       """
       yield from sql_session_fixture('warehouse', 'sqlite:///')


Two-phase transactions
----------------------

If your application uses multiple databases or other transaction-aware systems
such as `repoze.filesafe <http://docs.repoze.org/filesafe/>`_, `AcidFS
<https://acidfs.readthedocs.org/en/latest/>`_, `pyramid_mailer
<https://pyramid-mailer.readthedocs.org/>`_ or `ZODB <http://www.zodb.org/>`_
you need to `two-phase commits
<http://en.wikipedia.org/wiki/Two-phase_commit_protocol>`_ to coordinate
transactions. You can enable these using the ``enable_sql_two_phase_commit``
configuration directive.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import configure_all_connections

   configure_all_connections(twophase=True)

For Pyramid application you can also do this through the configurator instance:

.. code-block:: python
   :linenos:

   def main(global_config, **settings):
       config = Configurator(settings=settings)
       config.include('pyramid_sqlalchemy')
       config.enable_sql_two_phase_commit()

.. warning::

   Please note that this is not supported for all SQL servers. PostgreSQL is
   the only server where this is guaranteed to work. SQL Server does support
   two -phase transactions, but the Python driver support for it is unusable.

