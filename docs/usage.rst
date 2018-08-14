Usage
=====


Initialisation
--------------

Initialisation is very easy: the only thing you need to do is to create an
:ref:`SQLAlchemy engine <sqlalchemy:engines_toplevel>`, normally by
providing a :ref:`database URL <sqlalchemy:database_urls>` to
:py:func:`sqlalchemy.create_engine`, and tell
pyramid_sqlalchemy about that using the
:py:func:`pyramid_sqlalchemy.bind_connection` function.

.. code-block:: python
   :linenos:

   from sqlalchemy import create_engine
   from pyramid_sqlalchemy import bind_connection

   engine = create_engine('sqlite://')
   bind_connection(engine)


ORM classes
-----------

SQLAlchemy provides an incredible :ref:`ORM
<sqlalchemy:ormtutorial_toplevel>` to interact with databases. To use
this with pyramid_sqlalchemy the only thing you need to remember is to
use the `pyramid_sqlalchemy.orm_base` function to get the base classes for
mapped classes.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import orm_base
   from sqlalchemy import Column Integer, String

   class User(Base):
       __tablename__ = 'users'

       id = Column(Integer, primary_key=True)
       name = Column(String)
       fullname = Column(String)
       password = Column(String)


Metadata
--------

If you do want want to use the ORM you can also use SQLAlchemy core constructs
using a provided metadata instance.

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_metadata
   from sqlalchemy import Column, Table, Integer, String

   user = Table('user', get_metadata(),
       Column('user_id', Integer, primary_key=True),
       Column('user_name', String(16), nullable=False),
       Column('email_address', String(60)),
       Column('password', String(20), nullable=False)
   )


Performing a query
------------------

In order do a query you need to request the current session first, using the
:py:func:`pyramid_sqlalchemy.get_sql_session` function:

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_sql_session

   users = get_sql_session().query(User)
   for user in users:
       print('Hello %s' % user.user_name)

As a slight convenience you can also get a query instance directly with the
:py:func:`pyramid_sqlalchemy.get_sql_query` function:

.. code-block:: python
   :linenos:

   from pyramid_sqlalchemy import get_sql_query

   users = get_sql_query(User)
   for user in users:
       print('Hello %s' % user.user_name)

``get_sql_query`` will become more useful if you start using multiple
connections, but that is an advanced topic.
