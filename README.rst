.. image:: https://travis-ci.org/wichert/pyramid_sqlalchemy.svg?branch=master
    :target: https://travis-ci.org/wichert/pyramid_sqlalchemy

`pyramid_sqlalchemy` provides some basic glue to facilitate using
`SQLAlchemy <http://www.sqlalchemy.org/>`_ with `Pyramid
<http://docs.pylonsproject.org/projects/pyramid/en/latest/>`_.

SQLAlchemy relies on global state for a few things: 

* A ``MetaData`` instance which tracks all known SQL tables.
* A base class for all models using the ORM.
* A session factory.

Every application using SQLAlchemy must provides its own instance of these.
This makes it hard create add-on packages that also use SQLAlchemy, since they
either need to have their own SQLAlchemy state, which makes it hard to
integrate them into your application, or they need to jump through multiple
complex hoops to allow them share state with your application.

pyramid_sqlalchemy helps by providing a canonical location for the global
SQLAlchemy state. In addition it provides a convenient way to configure
SQLAlchemy in a Pyramid application.

::

    from pyramid.config import Configurator
    from pyramid_sqlalchemy import BaseObject

    class MyModel(BaseObject):
        __tablename__ = 'my_model'
        ...

    def main():
        config = Configurator()
        # Configure SQLAlchemy using settings from the .ini file
        config.include('pyramid_sqlalchemy')
        ...
        return config.make_wsgi_app()
