Usage
=====

The ORM base class is available as :py:class:`pyramid_sqlalchemy.meta.BaseObject`
and can be included directly:

.. code-block:: python

   from pyramid_sqlalchemy.meta import BaseObject

   class Account(BaseObject):
       __tablename__ = 'account'
       # Define your columns and methods here.


When you need to build a query you can use the
:py:obj:`pyramid_sqlalchemy.meta.Session` session factory. 

.. code-block:: python

   from pyramid_sqlalchemy.meta import Session

   account = Session.query(Account).first()

When writing methods in a model it is recommended to use
:py:func:`sqlalchemy.orm.session.object_session` instead:

.. code-block:: python

   from sqlalchemy.orm.session import object_session

   class Account(BaseObject):
       def favourites(self):
           "Return all the recent favourite articles."""
           session = object_session(self)
           return session.query(Article).all()
