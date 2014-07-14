Changelog
=========

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
