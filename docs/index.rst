`pyramid_sqlalchemy` provides some basic glue to facilitate using
`SQLAlchemy <http://www.sqlalchemy.org/>`_ over multiple packages,
and integration with `Pyramid
<http://docs.pylonsproject.org/projects/pyramid/en/latest/>`_.

SQLAlchemy relies on global state for a few things:

* A :ref:`MetaData <sqlalchemy:metadata_toplevel>` instance which tracks all
  known SQL tables.
* A :ref:`ORM base class <sqlalchemy:declarative_toplevel>` for all models using the ORM.
* A :ref:`session factory <sqlalchemy:unitofwork_contextual>`.

Every application using SQLAlchemy and its must provides its own instance of these.
This makes it hard create add-on packages that also use SQLAlchemy, since they
either need to have their own SQLAlchemy state, which makes it hard to
integrate them into your application, or they need to jump through multiple
complex hoops to allow them share state with your application.

pyramid_sqlalchemy helps by providing a canonical location for the global
SQLAlchemy state.

For advanced users it also supports multiple databases, with different tables
for each database.

This is a minimal example showing SQLAlchemy use in a pyramid application:


.. code-block:: python
   :linenos:

   from pyramid.config import Configurator
   from pyramid_sqlalchemy import orm_base

   class MyModel(orm_base()):
       __tablename__ = 'my_model'
       ...

   def main(global_config, **settings):
       config = Configurator(settings=settings)
       # Configure SQLAlchemy using settings from the .ini file
       config.include('pyramid_sqlalchemy')
       ...
       return config.make_wsgi_app()


Contents
========

.. toctree::
   :maxdepth: 1

   usage
   transactions
   pyramid
   tests
   advanced
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
