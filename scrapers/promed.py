import requests
from bs4 import BeautifulSoup

# _URL="http://www.promedmail.org/ajax/getPosts.php?edate=2017-01-01&return_map=0&feed_id=26&seltype=latest"
_DTSTART=""
_DTEND=""
_PAGENUM=1
_URL="http://www.promedmail.org/ajax/runSearch.php?kwby1=summary&kwby2=content&search=&date1=01%2F01%2F2016&date2=04%2F13%2F2017&feed_id=26"
# _URL="http://www.promedmail.org/ajax/runSearch.php?pagenum=7&kwby1=summary&kwby2=content&search=surto&date1=01%2F01%2F2016&date2=04%2F13%2F2017&feed_id=26&submit=next"

#LINK POST
# _URL_POST=http://www.promedmail.org/ajax/getPost.php?alert_id=3941627

r = requests.get(_URL)
content=r.json()['return']
# print(content)
soup = BeautifulSoup(content, "html5lib")

lis = soup.find_all('li')

form = soup.find('form')
LAST_PAGE=form.text.split("of")[1].strip()
print(LAST_PAGE)

if(len(lis)>0):

    for l in lis:
        print(l)
        a = l.find('a')
        # print(l.text)
        print(a['id'].replace("id",""))
        print(a.text)

#
