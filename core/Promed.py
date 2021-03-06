import requests
from bs4 import BeautifulSoup
from time import strptime
import re
import datetime
from core import InfoExtractor
from core import RedisNLP
import time
from datetime import datetime, timedelta


class Promed(object):

    def __init__(self,key_promed='promed', start = "01%2F01%2F2014", today=False, auto_period=True ,sleep=2):

        self.redis = RedisNLP(db=1)
        self.key_promed = key_promed

        # is automatic process
        if auto_period:
            self.define_period()

        #if defined processo today
        if today:
            self.start = self.end

        self.pagenum=-1
        self.URL = self.build_url(self.pagenum,self.start, self.end)
        print(self.URL)

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

        # scrap
        def scrap_li(lis):
            # loop over each LI tag with all informations about the health alerts
            for l in lis:
                print(l)
                a = l.find('a')
                print(a)
                if a != None:
                    obj = {}
                    obj['data'] = datetime.strptime(l.contents[0].strip().strip('\ufeff'), "%d %b %Y")
                    obj['datascrap'] = datetime.today().strftime("%d-%m-%Y")
                    obj['text'] = a.text
                    obj['id'] = a['id'].replace("id", "")
                    obj['link'] = 'http://www.promedmail.org/ajax/getPost.php?alert_id=%s' % (obj['id'])
                    obj['week'] = obj['data'].isocalendar()[1]
                    obj['content'], obj['urls'] = self.scrap_post(self.reader(obj['link'], key='post'))
                    # print(str(obj))
                    self.redis.get_redis().lpush(self.key_promed, obj)
                    # try:
                    #     print(obj['urls'][0])
                    #     self.redis.get_redis().lpush(self.key_promed, obj['urls'][0])
                    # except ValueError:
                    #     print(ValueError)

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
        content = content.split("Data: ")[1]
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

    def define_period(self):
        if self.len_promed()==0:
            self.start = "01%2F01%2F2014"
        else:
            self.start = (datetime.today() - timedelta(days=1)).strftime("%m-%d-%Y").replace("-", "%2F")
        #
        self.end = datetime.today().strftime("%m-%d-%Y").replace("-", "%2F")

# promed = Promed(start= (datetime.today() - timedelta(days=100)).strftime("%m-%d-%Y").replace("-","%2F"))
# promed.scrap()
#
# d = "02-05-2017"
# print(d)
# print(datetime.strptime(d, "%d-%m-%Y"))
# print((datetime.strptime(d, "%d-%m-%Y") - timedelta(days=1)))
# print((datetime.strptime(d, "%d-%m-%Y") - timedelta(days=1)).strftime("%d-%m-%Y"))

# d=("﻿15 Apr 2017").strip('\ufeff')
# print(d)
# print(datetime.strptime(d, "%d %b %Y").date().day)
