import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files

def main():
	soup = request.get_content_parsed_with_iso_encoding("http://www.senadoctes.gov.ar/senadores.htm")
	nombreCandidatos = parseNombreCandidatos(soup)
	senadores = list(map(lambda x: parseCandidato(x), nombreCandidatos))
	files.save_as_json('sources/corrientes/senadores.json', senadores)


def parseNombreCandidatos(soup):
	children = soup.find("select").find_all("option")
	candidates = list(map(lambda x: x["value"], children))
	return candidates[1:len(candidates)]
	

def parseCandidato(nombreCandidato):
	data = {}
	soup = request.get_content_parsed("http://www.senadoctes.gov.ar/" + nombreCandidato)
	tds= soup.find_all("td", class_="arryabaazul")
	data["img"] = "http://www.senadoctes.gov.ar/" + tds[0].find("img")["src"]
	strongTags = tds[1].find_all("font")
	data["nombre"] = strongTags[0].text.replace("\n","").strip().split(":")[1].strip()
	data["mandato"] = strongTags[2].text.replace("\n","")
	return data


if __name__ == "__main__":
	main()

