# -*- coding: utf-8 -*-
from py2neo import Graph
from py2neo.ogm import *


class Connection():
    graph=None

    @staticmethod
    def get_connection():
        if Connection.graph==None:
            HOSTNAME = "http://neo4j:7474/db/data"
            USER = "neo4j"
            PASS = "epitrack"
            Connection.graph = Graph(HOSTNAME, user=USER, password=PASS)
        return Connection.graph

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
    concordance = RelatedFrom("Concordance", "HAS_CONCORDANCE")

class Keyword(GraphObject):
    __primarykey__ = "name"
    name = Property()
    derivation = Property()

    keyword_alert = RelatedTo(Alert)

class Symptom(GraphObject):
    __primarykey__ = "name"
    name = Property()

    symptom_alert = RelatedTo(Alert)
    symptom_disease = RelatedTo(Disease)
    concordance = RelatedFrom("Concordance", "HAS_CONCORDANCE")

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
    concordance = RelatedFrom("Concordance", "HAS_CONCORDANCE")

class Concordance(GraphObject):
    __primarykey__ = "phrase"
    phrase=Property()

    symptom_concordance = RelatedTo(Symptom)
    disease_concordance = RelatedTo(Disease)
    city_concordance = RelatedTo(City)

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

# print(Connection.get_connection().run("MATCH (a) RETURN a LIMIT 4").data())