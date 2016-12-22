import deform
import colander as c
from pyramid.config import Configurator
from pyramid_sqlalchemy import (BaseObject, Session)
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText, )
from sqlalchemy.orm import relationship
from rebecca.search import sa_col
prefectures = [(), ]


class Address(BaseObject):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    prefecture = Column(Unicode(255))
    city = Column(Unicode(255))
    street = Column(Unicode(255))
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', backref='addresses')


class Person(BaseObject):
    __tablename__ = 'person'
    query = Session.query_property()
    id = Column(Integer, primary_key=True)
    last_name = Column(Unicode(255))
    first_name = Column(Unicode(255))
    description = Column(UnicodeText)
    birthday = Column(Date())


class PersonSearchSchema(c.MappingSchema):
    name = c.SchemaNode(sa_col(Person.first_name).contains(c.String()))


class SearchView:
    def __init__(self, request):
        self.request = request

    def search(self):
        form = deform.Form(PersonSearchSchema())
        people = []
        try:
            params = form.validate(self.request.params.items())
            people = Person.query.filter(*[
                condition() for condition in params.values()
                if condition != c.null
            ]).all()
            self.request.environ.setdefault('paste.testing_variables',
                                            {})['people'] = people
        except deform.ValidationFailure as e:
            form = e.field
        return dict(form=form, people=people)


def make_app(global_conf, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_sqlalchemy')
    config.add_jinja2_renderer('.html')
    config.add_view(SearchView, attr="search", renderer="search.html")
    return config.make_wsgi_app()
