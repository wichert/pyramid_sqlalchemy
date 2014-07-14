Initialisation
==============

When using pyramid_sqlalchemy in a Pyramid application you can easily configure
it by using the ``includeme`` function of the Pyramid configurator object:

.. code-block:: python
   :linenos:

   from pyramid.config import Configurator

   def main(global_config, **settings):
       config = Configurator(settings=settings)
       # Configure SQLAlchemy using settings from the .ini file
       config.include('pyramid_sqlalchemy')

This will pick up any ``sqlalchemy.*`` entries from your ``.ini`` file and
use those to configure SQLAlchemy. In particular the ``sqlalchemy.url``
entry is used, which must contain a :ref:`database URL
<sqlalchemy:database_urls>`.

For non-Pyramid applications or special situations you can also use
:py:func:`pyramid_sqlalchemy.init_sqlalchemy` to configure a SQLAlchemy engine
directly:

.. code-block:: python
   :linenos:

   from sqlalchemy import create_engine
   from pyramid_sqlalchemy import init_sqlalchemy

   engine = create_engine('sqlite://')
   init_sqlachemy(engine)


Two-phase transactions
----------------------

If your application uses both SQL and other transaction-aware systems such as
`repoze.filesafe <http://docs.repoze.org/filesafe/>`_, `AcidFS
<https://acidfs.readthedocs.org/en/latest/>`_, `pyramid_mailer
<https://pyramid-mailer.readthedocs.org/>`_ or `ZODB <http://www.zodb.org/>`_
you need to `two-phase commits
<http://en.wikipedia.org/wiki/Two-phase_commit_protocol>`_ to coordinate
transactions. You can enable these using the ``enable_sql_two_phase_commit``
configuration directive.

.. code-block:: python
   :linenos:

   def main(global_config, **settings):
       config = Configurator(settings=settings)
       config.include('pyramid_sqlalchemy')
       config.enable_sql_two_phase_commit()

Please note that this is not supported for all SQL servers. PostgreSQL is
the only server where this is guaranteed to work. SQL Server does support
two-phase transactions but the Python driver support for it is unusable.
The cx_oracle `supports them with some caveats
<https://docs.sqlalchemy.org/en/rel_0_9/dialects/oracle.html#two-phase-transaction-support>`_.
