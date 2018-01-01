import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
import re

from modules import request
from modules import files

def main():
	terceraPosicion = getDiputadosByBloque("http://www.diputados-catamarca.gov.ar/institucional/bloque-frente-tercera-posicion.html", "Frente Tercera Posición")
	frenteParaLaVictoria = getDiputadosByBloque("http://www.diputados-catamarca.gov.ar/institucional/bloque-frente-para-la-victoria.html", "Frente para la Victoria")
	frenteCivicoYSocial = getDiputadosByBloque("http://www.diputados-catamarca.gov.ar/institucional/bloque-frente-civico-y-social.html", "Frente Cívico y Social")
	participacionPlural = getDiputadosByBloque("http://www.diputados-catamarca.gov.ar/institucional/bloque-participacion-plural.html", "Participación Plural")
	cristinaConduccion = getDiputadosByBloque("http://www.diputados-catamarca.gov.ar/institucional/bloque-cristina-conduccion.html", "Cristina Conducción")
	files.save_as_json('sources/catamarca/diputados.json', terceraPosicion + frenteParaLaVictoria + frenteCivicoYSocial + participacionPlural + cristinaConduccion)

def getDiputadosByBloque(url, nombreBloque):
	soup = request.get_content_parsed(url)
	return __parse(soup, nombreBloque)

def __parse(soup, nombreBloque):
	candidates = []
	children = soup.find("div", class_="art-postcontent art-postcontent-0 clearfix").find_all("img")
	for child in children:
		data = {}
		imgSrc = child["src"]
		data["img"] = "http://www.diputados-catamarca.gov.ar/" + imgSrc[3: len(imgSrc)]
		parent = child.parent.parent if (child.parent.name == "p") else child.parent.parent.parent
		data["nombre"] = parent.contents[2].text.split("Dip.")[1].strip()
		mandato = parent.find(string=re.compile("Mandato")).strip().replace(" ", "").replace(":", "")
		data["mandato"] = mandato[7:len(mandato)]
		data["bloque"] = nombreBloque
		candidates.append(data)
	return candidates

if __name__ == "__main__":
	main()

