import deform
import colander as c
from pyramid.config import Configurator
from pyramid_sqlalchemy import (BaseObject, Session)
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText, )
from sqlalchemy.orm import relationship
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


class SearchSchema(c.MappingSchema):
    name = c.SchemaNode(c.String())


class SearchForm(deform.Form):
    def search(self, request, query):
        controls = request.params.items()
        params = self.validate(controls)
        expressions = [e() for e in params.values()]
        return query.filter(*expressions)


class SearchView:
    def __init__(self, request):
        self.request = request

    def search(self):
        return dict()


def make_app(global_conf, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.add_view(SearchView, attr="search", renderer="search.html")
    return config.make_wsgi_app()
