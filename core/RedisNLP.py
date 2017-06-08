# -*- coding: utf-8 -*-
import redis
import pickle
import json
import csv
import os
import ast

class RedisNLP(object):
    _conn = {}

    def __init__(self,key_diseases='diseases',key_state_cities='state_cities',key_symptoms='symptoms', api_key_dandelion='fa6b964b7746486bab94cc0e44cc1801',key_dandelion='key_dandelion',
                 file_symptoms='/data/sintomas.csv', file_state_cities='/data/estados_cidades.json', file_diseases='/data/doencas.txt',db=0):

        self.file_diseases=file_diseases
        self.file_symptoms=file_symptoms
        self.file_state_cities=file_state_cities
        self.key_diseases=key_diseases
        self.key_symptoms=key_symptoms
        self.key_state_cities=key_state_cities
        self.key_dandelion=key_dandelion
        self.api_key_dandelion=api_key_dandelion
        self.db=db
        self.r = RedisNLP.conn(db)

    @staticmethod
    def conn(db_=0):
        try:
            c = RedisNLP._conn[db_]
        except:
            RedisNLP._conn[db_]=redis.StrictRedis(host='localhost', port=6379, db=db_)
        return RedisNLP._conn[db_]

    def get_symptoms(self):
        symptoms = self.get_(self.key_symptoms)
        if symptoms==None:
            symptoms = []
            file = os.path.dirname(__file__).replace("/core","")+self.file_symptoms
            print(file)
            with open(file, 'r') as csvfile:
                for row in csv.DictReader(csvfile):
                    symptoms.append(row['NOME'].strip())
            self.save_(self.key_symptoms,symptoms)
            #
            # print("symptoms",symptoms)
            return symptoms
        else:
            return symptoms

    def get_dandelion_key(self):
        key_ = self.get_(self.key_dandelion)
        if key_== None:
            key_ = self.api_key_dandelion
            self.save_(self.key_dandelion,key_)
            return key_
        else:
            return key_

    def get_diseases(self):
        diseases = self.get_(self.key_diseases)
        if diseases== None:
            diseases = []
            file = os.path.dirname(__file__).replace("/core", "") + self.file_diseases
            print(file)
            with open(file, 'r') as txtfile:
                for row in txtfile.readlines():
                    diseases.append(row.split("\t")[0].lower())
            self.save_(self.key_diseases, diseases)
            return diseases
        else:
            return diseases

    def get_state_cities(self):
        estado_cidade = self.get_(self.key_state_cities,convert=False)
        if estado_cidade == None:
            file = os.path.dirname(__file__).replace("/core", "") + self.file_state_cities
            estado_cidade = json.loads(open(file).read())
            #
            self.save_(self.key_state_cities, estado_cidade,convert=False)
            estado_cidade = self.get_(self.key_state_cities, convert=False)
            #
            o = eval(ast.literal_eval(json.dumps(str(
                estado_cidade.decode('utf-8').replace("'", "||").replace("\"", "'").replace("||","\"")))))
            estado_cidade = o
            return estado_cidade
        else:
            o = eval(ast.literal_eval(json.dumps(str(
                estado_cidade.decode('utf-8').replace("'", "||").replace("\"", "'").replace("||", "\"")))))
            estado_cidade = o
            return estado_cidade

    def save_(self,key, data, convert=True):
        _data = data
        if convert:
            _data = pickle.dumps(data)

        self.r.set(key, _data)

    def get_(self,key, convert=True):
        results = self.r.get(key)
        if results == None:
            return None

        if convert:
            return pickle.loads(results)
        else:
            return results

    def get_redis(self):
        return self.r
