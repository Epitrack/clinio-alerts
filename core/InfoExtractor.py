# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
import newspaper
from newspaper import ArticleException
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
from core.db import Disease, Keyword, Symptom, State, City, Image, Date, Brand, Domain, Alert,Connection,Concordance
import dateutil.parser
import re

class InfoExtractor(object):

    def __init__(self,URL,object_date,text=None,db_=1,key_extract="extract",lang='pt',num_commom_items=10, error_file_loc='../logs/error.log', get_geolocation=False):

        self.lang = lang
        self.URL = URL
        self.info={}
        self.has_run=False
        self.num_commom_items= num_commom_items
        self.get_geolocation = get_geolocation
        self.text=text
        #
        try:
            logging.basicConfig(filename=error_file_loc,level=logging.ERROR)
        except:
            logging.basicConfig(filename='error.log', level=logging.ERROR)
        #
        self.config_corpus()
        #
        self.redis = RedisNLP(db=db_)
        self.key_extract = key_extract
        self.object_date = object_date
        self.invalid=False

    def config_corpus(self):
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.stopwords.append('é')

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
        o = urlparse(self.URL)
        URL_DOMAIN = o.scheme + "://" + o.netloc
        if ".pt" not in o.netloc:
            self.info_domain()
            self.info_article()
            self.info_nlp()
            self.has_run=True
        else:
            self.invalid=True
        return

    def info_article(self):

        logging.info("Reading Article info : "+self.URL)
        print(self.URL)
        article = Article(self.URL)

        try:
            article.download()
        except Exception as e:
            article.download(self.text)

        try:
            article.parse()
            article.nlp()

            self.info['article']={}
            self.text = article.text
            self.info['article']['authors'] = article.authors
            self.info['article']['publish_date'] = article.publish_date
            if self.info['article']['publish_date']==None:
                self.info['article']['publish_date'] = self.extractDate(self.text)
            self.info['article']['title'] = article.title
            self.info['article']['text'] = self.text
            self.info['article']['top_image'] = article.top_image
            self.info['article']['movies'] = article.movies
            self.info['article']['authors'] = article.authors
            self.info['article']['keywords'] = article.keywords
            self.info['article']['summary'] = article.summary
        except ArticleException:
            self.info['article']={}
            self.info['article']['publish_date']=None

    def extractDate(self,text):
        p = re.compile(
            "[0-9]{2}-[0-9]{2}-[0-9]{4} | [0-9]{2}/[0-9]{2}/[0-9]{4} | [0-9]{2}-(?:Jan|Janeiro|Mar|Março|Maio|Jun|Junho|Jul|Julho|Ago|Agosto|Outubro|Out|Dez|Dezembro)-[0-9]{4}")
        datas = (p.findall(text))
        print(datas)
        d=self.object_date
        try:
            if len(datas)>0:
                d = (dateutil.parser.parse(str(datas[0]).strip()))
        except:
            pass

        return d

    def info_nlp(self):
        logging.info("Reading Article info : "+self.URL)
        try:
            self.info['nlp']={}
            self.info['nlp']['disease'] = self.extract_diseases(self.text)
            self.info['nlp']['most_commom_words'] = self.extract_most_commom_words(self.text)
            self.info['nlp']['symptoms'] = self.extract_symptoms(self.text)
            self.info['nlp']['state_cities'] = self.extract_state_cities(self.text)
        except:
            pass

    def print(self):
        try:
            if self.has_run and not self.invalid:
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
        except:
            print("Invalid URL ",self.URL)

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
        # print(states_cites)
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
        # print(estados_siglas)
        estados_encontrados = {}
        _sentences = self.sentences(text)
        estados_encontrados = (
        lambda estados_filtrados: {w: [s for s in _sentences if str(s).lower().find(w)>-1] for w in
                                   estados_filtrados})(estados_filtrados)
        estados_cidades_in_text = {}
        try:
            estados_encontrados = functools.reduce(lambda x, y: dict(x, **y), (
            list({x: estados_encontrados[x]} for x in estados_encontrados if len(estados_encontrados[x]) > 0)))
        except Exception as ex:
            print(str(ex))
            if("reduce() of empty sequence with no initial value" in str(ex)):
                # print(_sentences)
                EXCLUDE=["Campanha","Socorro","Feliz","Guaraná","Coluna","Batalha","Capela"]#,"Central","Jardim","Cristina","Martins","Assis"]
                for _e in siglas_cidades:
                    _cidades=[]
                    for e in siglas_cidades[_e]:
                        matching = [s for s in _sentences if s.find(e)>-1 and e not in EXCLUDE]
                        if len(matching)>0:
                            _cidades.append({"nome": e, "latlng": self.getLatLng(e), "refs": matching})

                    if len(_cidades)>0:
                        estados_cidades_in_text[estados_siglas[_e]] = {
                            "refs": [],
                            "cidades": _cidades
                        }
                estados_encontrados={}

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
                cidades.append({"nome": cidade, "latlng": self.getLatLng(cidade), "refs": refs})
            estados_cidades_in_text[UF] = {
                "refs": estados_encontrados[UF],
                "cidades": cidades
            }
        if len(estados_cidades_in_text) >= 3:
            ordered_estados_cidades_in_text=sorted(estados_cidades_in_text, key= lambda x: len(estados_cidades_in_text[x]['cidades']), reverse=True)
            aux = {}
            aux[ordered_estados_cidades_in_text[0]] = estados_cidades_in_text[ordered_estados_cidades_in_text[0]]
            estados_cidades_in_text=aux

        return estados_cidades_in_text

    def getLatLng(self,cidade):
        latlng = []
        try:
            latlng = geocoder.google(cidade).latlng
        except Exception as err:
            pass
        return latlng

    def concordance(word, sentences, context=100):
        out = []
        for sent in sentences:
            if word in sent:
                context = len(sent)
                pos = sent.index(word)
                left = ''.join(sent[:pos])
                right = ''.join(sent[pos + len(word):])
                s = str('%*s %s %-*s' % (context, left[-context:], str(word).strip(), context, right[:context])).strip()
                out.append(s)
        return out

    def derivation(self,word):
        stemmer = nltk.stem.RSLPStemmer()
        return stemmer.stem(word)

    def persist(self):
        try:
            if self.info['article']['publish_date'] != None and not self.invalid:

                SENTENCES = self.sentences(self.text)

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
                    keyword.derivation = self.derivation(keyword.name)
                    alert.keywords.add(keyword,{"qtd":m[1]})

                diseases = self.info['nlp']['disease']
                for d in diseases:
                    di = Disease()
                    di.name = d
                    for _c in self.concordance(d,SENTENCES):
                        _concord = Concordance()
                        _concord.phrase = _c
                        di.concordance.add(_concord)

                    alert.diseases.add(di)

                symptoms = self.info['nlp']['symptoms']
                for s in symptoms:
                    sy = Symptom()
                    sy.name = s

                    for _c in self.concordance(s,SENTENCES):
                        _concord = Concordance()
                        _concord.phrase = _c
                        sy.concordance.add(_concord)

                    alert.symptoms.add(sy)

                state_cities = self.info['nlp']['state_cities']
                if len(state_cities)==0 and self.lang=="pt":
                    self.redis.get_redis().lpush("no_alerts", self.info)
                else:
                    for sc in state_cities:
                        e = State()
                        e.name = sc
                        for c in state_cities[sc]['cidades']:
                            city = City()
                            city.name = c['nome']
                            city.latlng = c['latlng']
                            for _c in c['refs']:
                                _concord = Concordance()
                                _concord.phrase = _c
                                city.concordance.add(_concord)
                            e.cities.add(city)
                        alert.states.add(e)

                print('''
                ####################################################################################################
                SALVANDO ALERTA DE SAÚDE... %s
                ####################################################################################################
                '''%(alert.title))
                try:
                    _c = Connection()
                    _c.get_connection().push(alert)
                    self.redis.get_redis().lpush(self.key_extract, self.object_date)
                except ValueError as e:
                    print("ERRO : %s"%(str(e)))
        except:
            pass


#http://portalsaude.saude.gov.br/index.php/o-ministerio/principal/secretarias/svs/noticias-svs/28348-ministerio-da-saude-declara-fim-da-emergencia-nacional-para-zika-e-microcefalia

# import datetime
# i = InfoExtractor('http://noticias.r7.com/rio-de-janeiro/rj-mais-duas-mortes-por-febre-amarela-sao-confirmadas-no-estado-04042017', {'data': datetime.datetime(2017, 5, 7, 0, 0)}, b"Domingo, 07 de maio de 2017 Fonte: EBC [03/05/2017] [editado] <a href='http://radioagencianacional.ebc.com.br/geral/audio/2017-05/surto-de-gripe-em-manaus-ja-matou-dez-criancas-menores-de-5-anos'>http://radioagencianacional.ebc.com.br/geral/audio/2017-05/surto-de-gripe-em-manaus-ja-matou-dez-criancas-menores-de-5-anos</a>  Surto de gripe em Manaus j\xc3\xa1 matou 10 crian\xc3\xa7as menores de 5 anos ---------------------------------------------------------------------------------------- Manaus vive um surto de gripe e as complica\xc3\xa7\xc3\xb5es da doen\xc3\xa7a podem ser a causa das mortes de 10 crian\xc3\xa7as menores de 5 anos de idade, registradas em abril [2017], no Hospital Pronto Socorro Delphina Rinaldi Abdel Aziz.  Os pacientes apresentaram sintomas da S\xc3\xadndrome Respirat\xc3\xb3ria Aguda Grave (SRAG), como falta de ar, febre, coriza e tosse. Segundo o diretor presidente da Funda\xc3\xa7\xc3\xa3o de Vigil\xc3\xa2ncia Sanit\xc3\xa1ria (FVS), Bernardino Albuquerque, os casos est\xc3\xa3o sendo investigados e exames preliminares j\xc3\xa1 identificaram dois tipos de v\xc3\xadrus. 'Infelizmente dessas crian\xc3\xa7as que foram a \xc3\xb3bito n\xc3\xa3o foi coletado material. Foi coletado material de crian\xc3\xa7as que tamb\xc3\xa9m estavam internadas, em tratamento, naquele momento e identificamos dois tipos de v\xc3\xadrus: principalmente os v\xc3\xadrus Sincicial Respirat\xc3\xb3rio e o Influenza B', explicou Bernardino Albuquerque.  Ap\xc3\xb3s as mortes, medidas preventivas foram refor\xc3\xa7adas nas unidades de sa\xc3\xbade de Manaus, como explica o diretor presidente da funda\xc3\xa7\xc3\xa3o. 'N\xc3\xb3s tivemos um foco inicial de atua\xc3\xa7\xc3\xa3o dentro do Hospital Delphina, no que diz respeito ao alerta aos profissionais, no manejo desses pacientes, no sentido de colocar esses pacientes em um ambiente mais restrito e isolado, a quest\xc3\xa3o dos cuidados de lavar as m\xc3\xa3os durante a manipula\xc3\xa7\xc3\xa3o. Por estar envolvido o v\xc3\xadrus da Influenza B, est\xc3\xa1 sendo ofertada a medica\xc3\xa7\xc3\xa3o antiviral Tamiflu.'  Al\xc3\xa9m disso, toda a rede hospitalar pedi\xc3\xa1trica da capital amazonense foi orientada a dar atendimento priorit\xc3\xa1rio a pacientes com os sintomas da S\xc3\xadndrome Respirat\xc3\xb3ria Aguda Grave e a colher material para que a circula\xc3\xa7\xc3\xa3o dos v\xc3\xadrus seja monitorada.  Atualmente, de acordo com o diretor presidente da Funda\xc3\xa7\xc3\xa3o de Vigil\xc3\xa2ncia Sanit\xc3\xa1ria, 15 pessoas, entre adultos e crian\xc3\xa7as, est\xc3\xa3o internadas em unidades de sa\xc3\xbade da cidade, com suspeita de SRAG.  No hospital Delphina, 5 crian\xc3\xa7as permanecem em tratamento e o quadro de sa\xc3\xbade delas ainda inspira cuidados. Bernardino Albuquerque d\xc3\xa1 algumas orienta\xc3\xa7\xc3\xb5es \xc3\xa0 popula\xc3\xa7\xc3\xa3o que ajudam a prevenir a gripe. 'N\xc3\xb3s temos uma arma que \xc3\xa9 bastante efetiva que \xc3\xa9 a vacina. Estamos estimulando para que a popula\xc3\xa7\xc3\xa3o busque as unidades de sa\xc3\xbade para que vacine seus filhos. E como medidas preventivas individuais, evitar a aglomera\xc3\xa7\xc3\xa3o de pessoas neste momento, principalmente de crian\xc3\xa7as, a quest\xc3\xa3o da higiene pessoal, de lavar as m\xc3\xa3os que \xc3\xa9 extremamente importante', explicou.  -- Comunicado por: ProMED-Port <a href='http://promedmail.org/pt'>http://promedmail.org/pt</a></p><p><h2>Veja tamb\xc3\xa9m</h2>\nProMED-PORT ----------- 2017: ano 20 do ProMED-PORT  Visite nosso site: <a href='http://www.promedmail.org/pt'>http://www.promedmail.org/pt</a>  Envie not\xc3\xadcias, informa\xc3\xa7\xc3\xb5es e coment\xc3\xa1rios: <a href='http://www.promedmail.org/submitinfo/'>http://www.promedmail.org/submitinfo/</a>  Inscreva um colega no ProMED-PORT: <a href='http://ww4.isid.org/promedmail/subscribe.php'>http://ww4.isid.org/promedmail/subscribe.php</a>  Fa\xc3\xa7a sua doa\xc3\xa7\xc3\xa3o ao ProMED: <a href='http://isid.org/donate/PMM_donate.shtml'>http://isid.org/donate/PMM_donate.shtml</a> .................................................RNA</p>")
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


