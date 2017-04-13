import requests
from bs4 import BeautifulSoup


_URL="http://www.healthmap.org/getAlerts.php?locations=&diseases=&sources%5B%5D=1&sources%5B%5D=7&sources%5B%5D=15&sources%5B%5D=12&sources%5B%5D=18&sources%5B%5D=24&sources%5B%5D=26&species=&category%5B%5D=1&category%5B%5D=2&category%5B%5D=29&vaccines=&time_interval=1+week&zoom_lat=15.000000&zoom_lon=18.000000&zoom_level=2&displayapi=&heatscore=1"

r = requests.get(_URL)
content=r.json()
for m in content['markers']:
    if m['place_name'].find('Brazil')!=-1:
        print m

# soup = BeautifulSoup(content, "html5lib")
