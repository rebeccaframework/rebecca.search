from datetime import date
import pytest
import webtest
from app import make_app


@pytest.fixture
def app(monkeypatch, sql_session):
    monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)
    settings = {}
    app = make_app({}, **settings)
    app = webtest.TestApp(app, extra_environ={'repoze.tm.active': True})
    return app


@pytest.fixture
def dummy_people(app, sql_session):
    from app import Person
    people = []
    for i in range(10):
        person = Person(
            first_name='person %d' % i,
            last_name="dummy",
            birthday=date(1970, 1, i + 1))
        sql_session.add(person)
        people.append(person)
    sql_session.flush()
    return people


def test_app(app, dummy_people, sql_session):
    res = app.get('/?name=3')
    assert res.people == [dummy_people[3]]
