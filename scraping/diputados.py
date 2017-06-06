from bs4 import BeautifulSoup

import requests
import json

def main():
	soup = get_content("http://www.diputados.gov.ar/diputados/listadip.html")	
	candidates = parse_candidates(soup)
	with open('sources/diputados.json', 'w') as outfile:
	    json.dump(candidates, outfile, ensure_ascii=False)




def parse_candidates(soup):
	contents = soup.find_all("td")
	candidates = []
	for i in range(0, len(contents), 6):
		data = {}
		data["img"] = contents[i].contents[0]["src"].encode('utf-8')
		nombre = contents[i + 1].contents[0].text.encode('utf-8').strip().split(",")
		data["apellido"] = nombre[0].strip()
		data["nombre"] = nombre[1].strip()
		data["distrito"] = contents[i + 2].text.encode('utf-8').strip()
		data["fechaInicioMandato"] = contents[i + 3].text.encode('utf-8')
		data["fechaFinMandato"] = contents[i + 4].text.encode('utf-8')
		data["partido"] = contents[i + 5].text.encode('utf-8')
		candidates.append(data)
	return candidates


def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	data = r.text.encode('utf-8')
	return BeautifulSoup(data, 'html.parser')

if __name__ == "__main__":
    main()
