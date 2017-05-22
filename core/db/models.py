# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship
from py2neo.ogm import *


class Connection():

    def __init__(self):
        self.HOSTNAME = "http://localhost:7474/db/data"
        self.USER = "neo4j"
        self.PASS = "epitrack"
        self.graph = Graph(self.HOSTNAME, user=self.USER, password=self.PASS)

    def get_connection(self):
        return self.graph

class Alert(GraphObject):
    __primarykey__ = "title"
    title = Property()
    text = Property()
    summary = Property()

    states = RelatedFrom("State", "IN_STATE")
    cities = RelatedFrom("City", "IN_CITY")
    symptoms = RelatedFrom("Symptom", "HAS_SYMPTOM")
    diseases = RelatedFrom("Disease", "HAS_DISEASE")
    domains = RelatedFrom("Domain", "IN_DOMAIN")
    brands = RelatedFrom("Brand", "IN_BRAND")
    keywords = RelatedFrom("Keyword", "HAS_KEYWORD")
    images = RelatedFrom("Image", "TOP_IMAGE")
    dates = RelatedFrom("Date", "IN_DATE")

class Disease(GraphObject):
    __primarykey__ = "name"
    name = Property()

    disease_alert = RelatedTo(Alert)
    symptoms = RelatedFrom("Symptom", "IN_SYMPTOM")

class Keyword(GraphObject):
    __primarykey__ = "name"
    name = Property()

    keyword_alert = RelatedTo(Alert)

class Symptom(GraphObject):
    __primarykey__ = "name"
    name = Property()

    symptom_alert = RelatedTo(Alert)
    symptom_disease = RelatedTo(Disease)

class State(GraphObject):
    __primarykey__ = "name"
    name = Property()

    cities = RelatedFrom("City", "IN_CITY")
    state_alert = RelatedTo(Alert)

class City(GraphObject):
    __primarykey__ = "name"
    name = Property()
    latlng = Property()

    city_alert = RelatedTo(Alert)
    city_state = RelatedTo(State)


class Image(GraphObject):
    __primarykey__ = "url"
    url = Property()

    image_alert = RelatedTo(Alert)

class Date(GraphObject):
    __primarykey__ = "date"
    date = Property()
    dia = Property()
    mes = Property()
    diames = Property()
    ano = Property()

    date_alert = RelatedTo(Alert)

class Brand(GraphObject):
    __primarykey__ = "name"
    name = Property()

    domains = RelatedFrom("Domain", "IN_DOMAIN")
    brand_alert = RelatedTo(Alert)

class Domain(GraphObject):
    __primarykey__ = "description"
    description = Property()
    size = Property()
    categories = Property()

    domain_alert = RelatedTo(Alert)
    domain_brand = RelatedTo(Brand)




