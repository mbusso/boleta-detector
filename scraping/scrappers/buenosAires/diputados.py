import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files


def main():
	diputados = files.readJsonFile("sources/provinciales/diputadosBuenosAires.aux.json")
	info = []
	for diputado in diputados:
		info.append(getAdditionalInfo(diputado))
	files.save_as_json('sources/provinciales/diputadosBuenosAires.json', info)


def getAdditionalInfo(diputado):
	url = "https://www.hcdiputados-ba.gov.ar/includes/undiputado.php?c_codigo={}&urlImagen=&incluyeIncludes=includes/".format(diputado["codigo"])
	soup = request.get_content_parsed(url)
	diputadoInfo = parse(soup)
	diputadoInfo["img"] = diputado["img"]
	diputadoInfo["codigo"] = diputado["codigo"]
	return diputadoInfo


def parse(soup):
	candidate = {}
	headers = soup.find_all("h5")
	candidate["nombre"] = headers[1].text.encode('utf-8').strip()
	bloqueToken = headers[2].text.encode('utf-8').replace("\t","").replace("  "," ").strip().split(":")
	candidate["bloque"] = bloqueToken[1].replace("\xc2\xa0 \r\n","")
	candidate["rol"] = "Diputado"
	candidate["proyectosPresentados"] = soup.find("a", class_ ="link_verde")["href"]
	distritoIndex = 3 if len(soup.find("div", class_="informe")) == 17 else 5
	candidate["distrito"] = soup.find("div", class_="informe").contents[distritoIndex].text.encode('utf-8').split(":")[1].replace("\t","").replace("\r","").replace("\n","").replace("\xc2\xa0","").strip()
	return candidate


if __name__ == "__main__":
    main()
