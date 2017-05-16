import redis
import pickle
import json
import csv

class RedisNLP(object):

    def __init__(self,key_diseases='diseases',key_state_cities='state_cities',key_symptoms='symptoms',
                 file_symptoms='../data/sintomas.csv', file_state_cities='../data/estados_cidades.json', file_diseases='../data/doencas.txt',db=0):

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
        if symptoms== None:
            symptoms = []
            with open(self.file_symptoms, 'r') as csvfile:
                for row in csv.DictReader(csvfile):
                    symptoms.append(row['NOME'].strip())
            self.save_(self.key_symptoms,symptoms)
            return symptoms
        else:
            return symptoms

    def get_diseases(self):
        diseases = self.get_(self.key_diseases)
        if diseases== None:
            diseases = []
            with open(self.file_diseases, 'r') as txtfile:
                for row in txtfile.readlines():
                    diseases.append(row.split("\t")[0].lower())
            self.save_(self.key_diseases, diseases)
            return diseases
        else:
            return diseases

    def get_state_cities(self):
        estado_cidade = self.get_(self.key_state_cities)
        if estado_cidade == None:
            estado_cidade = pickle.dumps(json.loads(open('data/estados_cidades.json').read()))
            self.save_(self.key_state_cities, estado_cidade, convert=False)
            return estado_cidade
        else:
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
# # r.get_redis().delete('diseases')
# print("get_state_cities")
# print(r.get_state_cities())
# print("get_diseases")
# print(r.get_diseases())
# print("get_symptoms")
# print(r.get_symptoms())


