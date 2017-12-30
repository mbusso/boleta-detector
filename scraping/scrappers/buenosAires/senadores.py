import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files

def main():
	soup = request.get_content_parsed("http://www.senado-ba.gov.ar/Senadores.aspx")
	senadores = parse(soup)
	files.save_as_json('sources/provinciales/senadoresBuenosAires.json', senadores)

def parse(soup):
	candidates = []
	children = soup.find_all("article", attrs={"data-ix":"show-portfolio-overlay"})
	for child in children:
	 	data = {}
		parent = child.find("a")
	 	data["additionalInfo"] = parent["href"]
		data["img"] = parent.find("img")["src"]
		data["nombre"] = parent.find("div", class_="Dato NombreSenador2").contents[2].encode('utf-8').strip()
		data["bloque"] = parent.find("div", class_="Dato BloqueSenador").contents[2].encode('utf-8').strip()
		data["distrito"] = parent.find_all("div", class_="Dato SeccionSenador")[1].contents[2].encode('utf-8').strip()
		data["mandato"] = parent.find_all("div", class_="Dato SeccionSenador")[2].contents[2].encode('utf-8').strip()
	  	candidates.append(data)
	return candidates

if __name__ == "__main__":
    main()

