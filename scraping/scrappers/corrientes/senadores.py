import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files

def main():
	soup = request.get_content_parsed("http://www.senadoctes.gov.ar/senadores.htm")
	nombreCandidatos = parseNombreCandidatos(soup)
	candidatos = map(lambda x: parseCandidato(x), nombreCandidatos)
	print(candidatos)


def parseNombreCandidatos(soup):
	children = soup.find("select").find_all("option")
	candidates = map(lambda x: x["value"].encode("utf-8"), children)
	return candidates[1:len(candidates)]
	

def parseCandidato(nombreCandidato):
	print nombreCandidato
	data = {}
	soup = request.get_content_parsed("http://www.senadoctes.gov.ar/" + nombreCandidato)
	tds= soup.find_all("td", class_="arryabaazul")
	data["img"] = tds[0].find("img")["src"]
	strongTags = tds[1].find_all("strong")
	print strongTags
	data["nombre"] = strongTags[0].text.encode('utf-8')
	data["mandato"] = strongTags[1].text.encode('utf-8')
	return data


if __name__ == "__main__":
	main()

