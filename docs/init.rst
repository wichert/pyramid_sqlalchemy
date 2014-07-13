Initialisation
==============

When using pyramid_sqlalchemy in a Pyramid application you can easily configure
it by using the ``includeme`` function of the Pyramid configurator object:

.. code-block:: python

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
