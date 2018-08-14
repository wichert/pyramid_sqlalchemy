from sqlalchemy import create_engine
from pyramid_sqlalchemy import init_sqlalchemy
from pyramid_sqlalchemy import Session


def test_basic_sqlite():
    engine = create_engine('sqlite://')
    init_sqlalchemy(engine)
    assert Session.session_factory.kw['bind'] is engine
