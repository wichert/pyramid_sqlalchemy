Changelog
=========

1.2 - Unreleased
-------------------

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
