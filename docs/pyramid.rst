Pyramid integration
===================

Configuration
-------------

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

You can also specify multiple connections in your configuration file. These will
be picked up automatically.

.. code-block:: ini
   :linenos:

   [app:main]
   use = egg:myapp
   # Configure the default SQL connection. This is equivalent to assigning
   # to sqlalchemy.default.url.
   sqlalchemy.url = postgresql://myapp
   # Configure the data warehouse
   sqlalchemy.warehouse.url = postgresql://data-warehouse.example.com/myapp


Request properties
------------------

As a convenience the current SQLAlchemy session is always available via the
``sql_session`` request property.

.. code-block:: python
   :linenos:

   from pyramid_views import view_config

   @view_config(route_name='users', renderer='json')
   def list_users(request):
      users = request.sql_session.query(User).order_by(User.user_name)
      return [
          {'id': user.user_id, 'name': user.user_name}
          for user in users
      ]

You can also get a query instance via the ``sql_query`` request method.

.. code-block:: python
   :linenos:

   from pyramid_views import view_config

   @view_config(route_name='users', renderer='json')
   def list_users(request):
      users = request.sql_query(User).order_by(User.user_name)
      return [
          {'id': user.user_id, 'name': user.user_name}
          for user in users
      ]
