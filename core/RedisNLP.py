# -*- coding: utf-8 -*-
import redis
import pickle
import json
import csv
import os
import ast
class RedisNLP(object):

    def __init__(self,key_diseases='diseases',key_state_cities='state_cities',key_symptoms='symptoms',
                 file_symptoms='/data/sintomas.csv', file_state_cities='/data/estados_cidades.json', file_diseases='/data/doencas.txt',db=0):

        self.file_diseases=file_diseases
        self.file_symptoms=file_symptoms
        self.file_state_cities=file_state_cities
        self.key_diseases=key_diseases
        self.key_symptoms=key_symptoms
        self.key_state_cities=key_state_cities
        self.db=db
        self.r = self.conn()

    def conn(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=self.db)
        return r

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
            # print("4 ",estado_cidade)
            # print("5 ", type(estado_cidade))
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

# r = RedisNLP()
# r.get_redis().delete('state_cities')
# print("get_state_cities")
# print(r.get_state_cities())
# print(type(r.get_state_cities()))
# print(r.get_state_cities()['estados'])
# print("get_diseases")
# print(r.get_diseases())
# print("get_symptoms")
# print(r.get_symptoms())


