import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files
import re


def main():
	soup = request.get_content_parsed("https://www.hcdiputados-ba.gov.ar/index.php?id=diputados&id_menu=mandatovigente")
	candidates = parse(soup)
	files.save_as_json('sources/provinciales/diputadosBuenosAires.aux.json', candidates)

def parse(soup):
	candidates = []
	children = soup.find_all("div", class_="derecha_un_tercio")
	for i in range(0, len(children)):
	 	data = {}
	 	nombreImagen = children[i].find("img")["src"].split("/")[2]
	 	data["codigo"] = nombreImagen[2: len(nombreImagen) - 4]
	 	data["img"] = children[i].find("img")["src"]
	 	data["nombre"] = children[i].find("div", class_="nombre_diputado").text.encode('utf-8')
	  	candidates.append(data)
	return candidates

if __name__ == "__main__":
    main()

