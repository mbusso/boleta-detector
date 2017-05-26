from bs4 import BeautifulSoup

import requests
import json

r  = requests.get("http://www.politicosonline.com/ranking")
r.encoding = 'utf-8'
data = r.text

soup = BeautifulSoup(data, 'html.parser')

paginationBlock = soup.find(id="pagination-digg").find_all("a")

def paginationNumbers(x): return str(x.text)

paginationNumbers = map(paginationNumbers, paginationBlock[0:5])
contents = soup.find(id="klout-top").find_all("tr")

candidates = []
for tr in contents[1: len(contents) -1]:
	tds = tr.find_all("td")
	data = {}
	data['img'] = tr.find_all("td")[0].contents[0]["src"]
	data['name'] = tr.find_all("td")[3].contents[0].text
	data['href'] = tr.find_all("td")[3].contents[0]["href"]
	data['amountOfFollowers'] = tr.find_all("td")[5].text
	data['description'] = tr.find_all("td")[6].text
	candidates.append(data)

with open('data.json', 'w') as outfile:
    json.dump(candidates, outfile)
	

#http://www.politicosonline.com/ranking?desde=250&orderby=klout