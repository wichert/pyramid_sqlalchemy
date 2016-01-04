Changelog
=========

1.6 - January 4, 2016
---------------------

- Update ``transaction`` pytest fixture to not mock out ``transation.get()``
  completely, but only the ``commit()`` transaction method. This fixes problems
  with code trying to write on the current transaction.


1.5 - December 30, 2015
-----------------------

- Fix a compatibility error with the DatabaseTestCase class which could break
  functional test setup.

- Code reorganisation: move tests outside the package; there is no point in
  installing them.


1.4 - November 25, 2015
-----------------------

- Revert naming convention change. This change broke all existing data models
  which did not supply a constraint name everywhere. This is especially bad
  for types which implicitly create unnamed constraints, such as booleans and
  enums on dialects that do not have native support.


1.3 - November 23, 2015
-----------------------

- Configure a default naming convention, as `recommended by alembic
  <http://alembic.readthedocs.org/en/latest/naming.html>`_).
  `Pull request 3 <https://github.com/wichert/pyramid_sqlalchemy/pull/3>`_
  from Marcin Lulek.

- Fix a broken import in pyramid_sqlalchemy's own test when running on Python 3.

- Allow overriding the database used for testing with the pytest ``--sql-url`` 
  option when using the ``DatabaseTestCase`` test class. For non-pytest users
  support the ``DB_URI`` environment variable as well.


1.2.2 - September 11, 2014
--------------------------

- Add dependency on mock for Python <3.3. This fixes import problems who try to
  import pyramid_sqlalchemy.testing in production code.


1.2.1 - September 1, 2014
-------------------------

- Move pyramid to a test-only dependency. This makes it simpler to use
  pyramid_sqlalchemy in non-pyramid contexts.


1.2 - August 30, 2014
---------------------

- Use `unittest.mock` when available. This removes the `mock` dependency on
  Python 3.

- Tests no longer need to mock out pyramid_sqlalchemy.includeme; this is now
  handled by ``DatabaseTestCase`` and the py.test fixtures.

- Automatically make py.test fixtures available externally. This removes the
  need to copy & paste them over from the documentation.

- Fix error on pytest fixture example.

- Setup `Travis <https://travis-ci.org/wichert/pyramid_sqlalchemy>`_ to
  automatically run tests on CPython 2.6, CPython 2.7, CPython 3.3, CPython 3.4
  and PyPy.


1.1 - July 14, 2014
-------------------

- Add missing schema to the Pyramid-URL in the package description. This broke
  ReST rendering on the PyPI page.

- Add a new ``enable_sql_two_phase_commit()`` configuration directive to enable
  two-phase commit.

- Enable foreign key constraint checking for SQLite in DatabaseTestCase.

- Use SQLAlchemy events instead of ZopeTransactionExtension to handle
  integration of zope.sqlalchemy and SQLAlchemy.


1.0 - July 13, 2014
-------------------

- First release.
