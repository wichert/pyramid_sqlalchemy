Changelog
=========

1.1 - Unreleased
-------------------

- Add missing schema to Pyramid-URL. This broke ReST rendering on the PyPI page.

- Add a new ``enable_sql_two_phase_commit()`` configuration directive enable
  two-phase commit.

- Enable foreign key constraint checking for SQLite in DatabaseTestCase.

- Use SQLAlchemy events instead of ZopeTransactionExtension to handle
  integration of zope.sqlalchemy and SQLAlchemy.


1.0 - July 13, 2014
-------------------

- First release.
