# -*- coding: utf-8 -*-
from py2neo import Graph
from py2neo.ogm import *


class Connection():
    graph=None

    @staticmethod
    def get_connection(HOSTNAME="http://neo4j:7474/db/data",USER = "neo4j",PASS = "epitrack"):
        if Connection.graph==None:
            Connection.graph = Graph(HOSTNAME, user=USER, password=PASS)
        return Connection.graph


class Concordance(GraphObject):
    __primarykey__ = "phrase"
    phrase=Property()

    disease = RelatedFrom("Disease", "HAS_CONCORDANCE")
    symptom = RelatedFrom("Symptom", "HAS_CONCORDANCE")
    city = RelatedFrom("City", "HAS_CONCORDANCE")

class Symptom(GraphObject):
    __primarykey__ = "name"
    name = Property()

    alert = RelatedFrom("Alert", "HAS_SYMPTOM")
    disease = RelatedFrom("Disease", "IN_SYMPTOM")

    concordances = RelatedTo(Concordance)


class City(GraphObject):
    __primarykey__ = "name"
    name = Property()
    latlng = Property()

    alert = RelatedFrom("Alert", "IN_STATE")
    state = RelatedFrom("State", "IN_CITY")

    concordances = RelatedTo(Concordance)

class Disease(GraphObject):
    __primarykey__ = "name"
    name = Property()

    alert = RelatedFrom("Alert", "HAS_DISEASE")

    symptoms = RelatedTo(Symptom)
    concordances = RelatedTo(Concordance)

class Keyword(GraphObject):
    __primarykey__ = "name"
    name = Property()
    derivation = Property()

    alert = RelatedFrom("Alert", "HAS_KEYWORD")

class State(GraphObject):
    __primarykey__ = "name"
    name = Property()

    alert = RelatedFrom("Alert", "IN_STATE")

    cities = RelatedTo(City)

class Image(GraphObject):
    __primarykey__ = "url"
    url = Property()

    alert = RelatedFrom("Alert", "TOP_IMAGE")

class Date(GraphObject):
    __primarykey__ = "date"
    date = Property()
    dia = Property()
    mes = Property()
    diames = Property()
    ano = Property()

    alert = RelatedFrom("Alert", "IN_DATE")

class Brand(GraphObject):
    __primarykey__ = "name"
    name = Property()

    domain = RelatedFrom("Domain", "IN_DOMAIN")
    alert = RelatedFrom("Alert", "IN_BRAND")

class Domain(GraphObject):
    __primarykey__ = "description"
    description = Property()
    size = Property()
    categories = Property()

    alert = RelatedFrom("Alert", "IN_DOMAIN")

    brands = RelatedTo(Brand)

class EntityCategories(GraphObject):
    __primarykey__ = "name"
    name=Property()

    entity = RelatedFrom("Entity", "HAS_ENTITY_CATEGORIES")

class EntityTypes(GraphObject):
    __primarykey__ = "name"
    name=Property()

    entity = RelatedFrom("Entity", "HAS_ENTITY_TYPES")

class Entity(GraphObject):
    __primarykey__ = "title"
    start=Property()
    end=Property()
    spot=Property()
    confidence=Property()
    title=Property()
    uri=Property()
    abstract=Property()
    label=Property()

    alerts = RelatedFrom("Alert", "HAS_ENTITY")

    categories = RelatedTo(EntityCategories)
    types = RelatedTo(EntityTypes)

class Alert(GraphObject):
    __primarykey__ = "title"
    title = Property()
    text = Property()
    summary = Property()
    url= Property()
    has_entities=Property()

    states = RelatedTo(State)
    cities = RelatedTo(City)
    symptoms = RelatedTo(Symptom)
    diseases = RelatedTo(Disease)
    domains = RelatedTo(Domain)
    brands = RelatedTo(Brand)
    keywords = RelatedTo(Keyword)
    images = RelatedTo(Image)
    dates = RelatedTo(Date)
    entities = RelatedTo(Entity)