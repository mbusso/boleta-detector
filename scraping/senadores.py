from bs4 import BeautifulSoup

import requests
import json

def main():
	soup = get_content("http://www.senado.gov.ar/senadores/listados/listaSenadoRes")
	candidates = parse_candidates(soup)
	with open('senadores.json', 'w') as outfile:
	    json.dump(candidates, outfile, ensure_ascii=False)


def parse_candidates(soup):
	candidates = []
	contents = soup.find_all("tr")
	for i in range(1, len(contents)):
		data = {}
		data["nombre"] = contents[i].contents[3].text.encode('utf-8').replace("\t","").replace("  "," ").strip()
		data["img"] = contents[i].contents[1].find("a").contents[1]["src"]
		data["href"] = contents[i].contents[1].find("a")["href"]
		data["provincia"] = contents[i].contents[5].text.encode('utf-8').strip(' \t\n\r')
		data["partido"] = contents[i].contents[7].text.encode('utf-8').strip(' \t\n\r')
		fechas = contents[i].contents[9].text.encode('utf-8').replace("<br/>","").strip(' \t\n\r').replace("\n"," ").split()
		data["fechaInicioMandato"] = fechas[0]
		data["fechaFinMandato"] = fechas[1]
		#data["facebook"] = contents[i].contents[11].find_all("a")[1]["href"]
		#data["twitter"] = contents[i].contents[11].find_all("a")[2]["href"]
		candidates.append(data)
	return candidates


def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	data = r.text.encode('utf-8')
	return BeautifulSoup(data, 'html.parser')

if __name__ == "__main__":
    main()