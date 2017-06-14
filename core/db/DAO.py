# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from core import RedisNLP
from py2neo import Graph, NodeSelector
from core.db import Disease, Keyword, Symptom, State, City, Image, Date, Brand, Domain, Alert,Connection,Concordance
graph = Connection.get_connection("http://169.57.140.234:7474/db/data")
selector = NodeSelector(graph)
# res = graph.data("MATCH (a:Alert{title:''}) RETURN a")
# res = selector.select("Alert").first()
# res = graph.data("MATCH (n) WHERE EXISTS(n.title) RETURN  n.title AS title")
# res = graph.data("MATCH (n) WHERE EXISTS(n.title) RETURN  n.title AS title, n.url")
# print(res)
# MATCH (n:Alert{title:'Surto de vômito e diarreia atinge cidades do Alto Oeste – Jornal O Mossoroense'}) RETURN  n.title AS title, ID(n)
