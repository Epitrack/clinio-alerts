import os, sys
lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
sys.path.append(lib_path)

import newspaper
from newspaper import Article
from urllib.parse import urlparse
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import string
import logging
import functools
import geocoder
from core import RedisNLP
from core.db import Disease, Keyword, Symptom, State, City, Image, Date, Brand, Domain, Alert, graph

class InfoExtractor(object):

    def __init__(self,URL,lang='pt',num_commom_items=10, error_file_loc='../logs/error.log', get_geolocation=False):

        '''
        :param URL:
        :param lang:
        :param num_commom_items:
        :param error_file_loc:
        :param get_geolocation:
        '''
        self.lang = lang
        self.URL = URL
        self.info={}
        self.has_run=False
        self.num_commom_items= num_commom_items
        self.get_geolocation = get_geolocation
        self.text=None
        #
        logging.basicConfig(filename=error_file_loc,level=logging.ERROR)
        #
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.stopwords.append('é')
        self.redis = RedisNLP()

    def info_domain(self):

        logging.info("Reading domain infos")

        self.info['domain']={}
        o = urlparse(self.URL)
        URL_DOMAIN = o.scheme + "://" + o.netloc
        site = newspaper.build(URL_DOMAIN, language=self.lang, memoize_articles=False)
        self.info['domain']['brand'] = site.brand
        self.info['domain']['description'] = site.description
        self.info['domain']['size'] = site.size()
        self.info['domain']['categories'] = site.category_urls()

    def run(self):
        self.info_domain()
        self.info_article()
        self.info_nlp()
        self.has_run=True
        return

    def info_article(self):

        logging.info("Reading Article info : "+self.URL)
        print(self.URL)
        article = Article(self.URL)
        article.download()

        while not article.is_downloaded:
            article.download()

        article.parse()
        article.nlp()

        self.info['article']={}
        self.info['article']['authors'] = article.authors
        self.info['article']['publish_date'] = article.publish_date
        self.info['article']['title'] = article.title
        self.info['article']['text'] = article.text
        self.text = self.info['article']['text']
        self.info['article']['top_image'] = article.top_image
        self.info['article']['movies'] = article.movies
        self.info['article']['authors'] = article.authors
        self.info['article']['keywords'] = article.keywords
        self.info['article']['summary'] = article.summary

    def info_nlp(self):
        logging.info("Reading Article info : "+self.URL)

        self.info['nlp']={}
        self.info['nlp']['disease'] = self.extract_diseases(self.text)
        self.info['nlp']['most_commom_words'] = self.extract_most_commom_words(self.text)
        self.info['nlp']['symptoms'] = self.extract_symptoms(self.text)
        self.info['nlp']['state_cities'] = self.extract_state_cities(self.text)

    def print(self):
        if self.has_run:
            print("\n======================================================\n")
            print("Extract URL: ",self.URL)
            print("\nDOMAIN INFORMATIONS:\n")
            print("Brand: ",  self.info['domain']['brand'])
            print("Description: ", self.info['domain']['description'])
            print("Size: ", self.info['domain']['size'])
            print("Categories: ", self.info['domain']['categories'])
            print("\nARTICLE INFORMATIONS:\n")

            print("Authors: ", self.info['article']['authors'])
            print("Publish Date: ", self.info['article']['publish_date'])
            print("Title: ", self.info['article']['title'])
            print("Text: ", self.info['article']['text'])
            print("Top Image: ", self.info['article']['top_image'])
            print("Movies: ", self.info['article']['movies'])
            print("Keywords: ", self.info['article']['keywords'])
            print("Summary: ", self.info['article']['summary'])

            print("\nNLP INFORMATIONS:\n")
            print("Disease: ", self.info['nlp']['disease'])
            print("Most Commom Words: ", self.info['nlp']['most_commom_words'])
            print("Symptoms: ", self.info['nlp']['symptoms'])
            print("State/Cities: ", self.info['nlp']['state_cities'])

            print("\n======================================================\n")

        else:
            print("Please, invoke run() function first")

    def getInfos(self):
        return self.info

    def read_symptoms(self):
        symptoms = self.redis.get_symptoms()
        return symptoms

    def read_disease(self):
        disease = self.redis.get_diseases()
        return disease

    def read_state_cities(self):
        states_cites = self.redis.get_state_cities()
        estados = states_cites['estados']

        estados_filtrados = (lambda estados: [str(w['nome']).lower() for w in estados])(estados)
        siglas_filtrados = (lambda estados: [str(w['sigla']) for w in estados])(estados)
        estados_siglas = (lambda estados: {w['sigla']: str(w['nome']).lower() for w in estados})(estados)
        siglas_cidades = (lambda estados: {w['sigla']: w['cidades'] for w in estados})(estados)

        return estados_filtrados, estados_siglas, siglas_filtrados,siglas_cidades

    def sentences(self,text):
        return sent_tokenize(text)

    def tokenizer(self, text):
        return word_tokenize(text)

    def extract_most_commom_words(self,text):
        try:
            text = "".join(l for l in text if l not in string.punctuation)
            text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)
            word_tokenize_list = word_tokenize(text)
            fd = nltk.FreqDist(w.upper() for w in word_tokenize_list if w.lower() not in self.stopwords)
            return fd.most_common(self.num_commom_items)
        except Exception as err:
            logging.error("{0}".format(err))
            pass

    def extract_symptoms(self,text):
        symptoms = self.read_symptoms();

        symptoms_in_text = {}
        for e in symptoms:
            matching = [s for s in self.sentences(text) if e in str(s).lower()]
            if len(matching) > 0:
                symptoms_in_text[e] = matching

        return symptoms_in_text


    def extract_diseases(self,text):
        diseases_in_text={}
        diseases = self.read_disease()
        for e in diseases:
            matching = [s for s in self.sentences(text) if e in str(s).lower()]
            if len(matching) > 0:
                diseases_in_text[e] = matching
        return diseases_in_text

    def extract_state_cities(self,text):
        estados_filtrados, estados_siglas, siglas_filtrados, siglas_cidades = self.read_state_cities()

        estados_encontrados = {}
        _sentences = self.sentences(text)
        estados_encontrados = (
        lambda estados_filtrados: {w: [s for s in _sentences if w in str(s).lower()] for w in
                                   estados_filtrados})(estados_filtrados)
        try:
            estados_encontrados = functools.reduce(lambda x, y: dict(x, **y), (
            list({x: estados_encontrados[x]} for x in estados_encontrados if len(estados_encontrados[x]) > 0)))
        except:
            pass

        estados_cidades_in_text = {}
        for UF in estados_encontrados:
            SIGLA = dict(filter(lambda item: item[1] == UF, estados_siglas.items())).popitem()[0]
            cidades_encontrados = {}
            for e in siglas_cidades[SIGLA]:
                matching = [s for s in _sentences if str(e).lower() in str(s).lower()]
                if len(matching) > 0:
                    cidades_encontrados[e] = matching
            cidades = []
            for cidade in cidades_encontrados:
                refs = cidades_encontrados[cidade]
                latlng = []
                try:
                    latlng = geocoder.google(cidade).latlng
                except Exception as err:
                    print(err)
                    pass
                cidades.append({"nome": cidade, "latlng": latlng, "refs": refs})
            estados_cidades_in_text[UF] = {
                "refs": estados_encontrados[UF],
                "cidades": cidades
            }
        return estados_cidades_in_text

    def persist(self):

        brand = Brand()
        brand.name = self.info['domain']['brand']
        brand.name = self.info['domain']['description']
        brand.name = self.info['domain']['size']
        #
        image = Image()
        image.url=self.info['article']['top_image']
        #
        date = Date()
        date.date = self.info['article']['publish_date'].strftime('%Y-%m-%d')
        d = date.date.split("-")
        date.ano = d[0]
        date.mes = d[1]
        date.dia = d[2]
        #
        alert = Alert()
        alert.title = self.info['article']['title']
        alert.text = self.info['article']['text']
        alert.summary = self.info['article']['summary']
        alert.brands.add(brand)
        alert.images.add(image)
        alert.dates.add(date)

        most_commom_words = self.info['nlp']['most_commom_words']
        for m in most_commom_words:
            keyword = Keyword()
            keyword.name = str(m[0]).lower()
            alert.keywords.add(keyword,{"qtd":m[1]})

        diseases = self.info['nlp']['disease']
        for d in diseases:
            di = Disease()
            di.name = d
            alert.diseases.add(di)

        symptoms = self.info['nlp']['symptoms']
        for s in symptoms:
            sy = Symptom()
            sy.name = s
            alert.symptoms.add(sy)

        state_cities = self.info['nlp']['state_cities']
        for sc in state_cities:
            e = State()
            e.name = sc
            for c in state_cities[sc]['cidades']:
                city = City()
                city.name = c['nome']
                city.latlng = c['latlng']
                e.cities.add(city)

            alert.states.add(e)

        graph.push(alert)

# i = InfoExtractor(URL="http://agenciabrasil.ebc.com.br/geral/noticia/2017-05/secretaria-de-saude-de-minas-investiga-11-mortes-com-suspeita-de-chikungunya")
# i.run()
# i.print()
# i.persist()
#
# i = InfoExtractor(URL="http://g1.globo.com/rio-de-janeiro/noticia/rj-vai-vacinar-a-populacao-em-todo-o-estado-contra-a-febre-amarela.ghtml")
# i.run()
# i.print()
# i.persist()
#
# i = InfoExtractor(URL="http://www.em.com.br/app/noticia/gerais/2017/03/09/interna_gerais,853083/mortes-de-14-macacos-com-suspeita-de-febre-amarela-sao-investigadas-em.shtml")
# i.run()
# i.print()
# i.persist()
#
# i = InfoExtractor(URL="http://g1.globo.com/bahia/noticia/2017/03/homem-de-46-anos-morre-vitima-de-raiva-na-bahia-1-caso-desde-2004.html")
# i.run()
# i.print()
# i.persist()
#
# i = InfoExtractor(URL="http://g1.globo.com/bemestar/noticia/doenca-da-urina-preta-foi-causada-por-intoxicacao-apos-ingestao-de-peixe-diz-estudo.ghtml")
# i.run()
# i.print()
# i.persist()


