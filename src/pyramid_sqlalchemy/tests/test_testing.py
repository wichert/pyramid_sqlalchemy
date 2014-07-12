import unittest
from pyramid_sqlalchemy import meta
import sqlalchemy.schema
import sqlalchemy.types


class DatabaseTestCaseTests(unittest.TestCase):
    def DatabaseTestCase(self, *a, **kw):
        from pyramid_sqlalchemy.testing import DatabaseTestCase

        class MockCase(DatabaseTestCase):
            def runTest(self):  # pragma: no cover
                pass

        return MockCase(*a, **kw)

    def test_tables_exist(self):
        from sqlalchemy.engine.reflection import Inspector
        from pyramid_sqlalchemy import meta

        testcase = self.DatabaseTestCase()
        try:
            testcase.setUp()
            inspector = Inspector.from_engine(meta.Session.bind)
            self.assertTrue('dummy' in inspector.get_table_names())
        finally:
            testcase.tearDown()

    def test_no_leakage(self):
        from pyramid_sqlalchemy import meta
        testcase = self.DatabaseTestCase()

        class Dummy(meta.BaseObject):
            __tablename__ = 'dummy'

            id = sqlalchemy.schema.Column(sqlalchemy.types.Integer(),
                    primary_key=True, autoincrement=True)


        try:
            testcase.setUp()
            meta.Session.add(Dummy())
            testcase.tearDown()
            testcase.setUp()
            self.assertEqual(meta.Session.query(Dummy).count(), 0)
        finally:
            testcase.tearDown()
