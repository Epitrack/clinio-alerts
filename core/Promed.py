# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
import requests
from bs4 import BeautifulSoup
import re
from core import RedisNLP
import time
from datetime import datetime, timedelta
import datetime
import ast
import json

class Promed(object):

    def __init__(self,key_promed='promed',key_extract='extract', start = "01%2F01%2F2015", today=False, auto_period=True ,sleep=2):

        self.redis = RedisNLP(db=1)
        self.key_promed = key_promed
        self.key_extract = key_extract

        # is automatic process
        if auto_period:
            self.define_period(start)

        #if defined processo today
        if today:
            self.start = self.end

        self.pagenum=-1
        self.URL = self.build_url(self.pagenum,self.start, self.end)
        self.isToday=False

        self.sleep = sleep

    def reader(self,URL,key='return',headers={'User-Agent': 'Mozilla/5.0','Content-Type': 'application/x-www-form-urlencoded',
                                              'X-Requested-With': 'XMLHttpRequest','Referer':'http://www.promedmail.org'}):
        print(URL)
        r = requests.Session().get(URL,headers=headers)
        try:
            content = r.json()[key]
        except:
            print('exc')
            content = r.text
        return content

    def build_url(self,pagenum,start,end):
        if pagenum==-1:
            return "http://www.promedmail.org/ajax/runSearch.php?kwby1=summary&search=&date1=%s&date2=%s&feed_id=26" % (start, end)
        else:
            return "http://www.promedmail.org/ajax/runSearch.php?pagenum=%d&kwby1=summary&search=&date1=%s&date2=%s&feed_id=26" % (pagenum, start, end)

    def scrap(self):

        if not self.isToday:
            # scrap
            def scrap_li(lis):
                # loop over each LI tag with all informations about the health alerts
                for l in lis:
                    print(l)
                    a = l.find('a')
                    print(a)
                    if a != None:
                        obj = {}
                        obj['data'] = datetime.datetime.strptime(l.contents[0].strip().strip('\ufeff'), "%d %b %Y")
                        obj['datascrap'] = datetime.date.today().strftime("%d-%m-%Y")
                        obj['text'] = a.text
                        obj['id'] = a['id'].replace("id", "")
                        obj['link'] = 'http://www.promedmail.org/ajax/getPost.php?alert_id=%s' % (obj['id'])
                        obj['week'] = obj['data'].isocalendar()[1]
                        obj['content'], obj['urls'] = self.scrap_post(self.reader(obj['link'], key='post'))
                        self.redis.get_redis().lpush(self.key_promed, obj)

            # first request
            soup = BeautifulSoup(self.reader(self.URL), "html5lib")
            lis = soup.find_all('li')
            form = soup.find('form')
            lis = soup.find_all('li')

            # form
            if (form!= None):
                pagenum = int(form.text.split("of")[1].strip())
                # loop over pages
                for p in list(reversed(range(pagenum))):
                    # build URL with countdown range
                    self.URL = self.build_url((p+1), self.start, self.end)
                    soup = BeautifulSoup(self.reader(self.URL), "html5lib")
                    lis = soup.find_all('li')
                    #If has LI tag
                    if (len(lis) > 0):
                        scrap_li(lis)
                    time.sleep(self.sleep)
            else:
                scrap_li(lis)

        print("\nFinalizou")

    def scrap_post(self,content):

        try:
            content = content.split("Data: ")[1]
        except IndexError:
            content = content.split("Fonte: ")[1]

        content = content.replace("<br />"," ")
        soup = BeautifulSoup(content, "html5lib")
        content_ = soup.getText()
        urls_ = self.extractUrl(content_)
        return (content.encode('utf-8').strip(),urls_)

    def extractUrl(self,content):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        return urls

    def write(self,file,content):
        with open(file+".txt", "w") as text_file:
            for c in content:
                text_file.write("%s"%(c))

    def len_promed(self):
        return self.redis.get_redis().llen(self.key_promed)

    def define_period(self,start):

        '''
        Verify last date for scrap alerts news
        if last date is today, do not nothing
        if last date is different today, get this date until
        :return:
        '''
        if self.redis.get_redis().llen(self.key_extract)==0:
            self.start = start
        else:
            o = eval(ast.literal_eval(json.dumps(str(
                self.redis.get_redis().lpop(self.key_extract).decode('utf-8').replace("'", "||").replace("\"", "'").replace("||","\"")))))

            if o['data'].strftime("%d-%m-%Y") < datetime.date.today().strftime("%d-%m-%Y"):
                self.start = o['data'].strftime("%m-%d-%Y").replace("-", "%2F")
            else:
                self.start = datetime.date.today().strftime("%m-%d-%Y").replace("-", "%2F")
                self.isToday=True

        self.end = datetime.date.today().strftime("%m-%d-%Y").replace("-", "%2F")

# promed = Promed(start= (datetime.date.today() - timedelta(days=10)).strftime("%m-%d-%Y").replace("-","%2F"))
# promed.scrap()