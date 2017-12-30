import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files


def main():
	senadores = files.readJsonFile("sources/catamarca/senadores.aux.json")
	info = []
	for senador in senadores:
		info.append(getAdditionalInfo(senador))
	files.save_as_json('sources/catamarca/senadores.json', info)


def getAdditionalInfo(senador):
	url = "https://www.senadodecatamarca.gob.ar" + senador["additionalInfo"]
	soup = request.get_content_parsed(url)
	senadorInfo = parse(soup)
	senadorInfo["img"] = senador["img"]
	senadorInfo["additionalInfo"] = senador["additionalInfo"]
	senadorInfo["bloque"] = senador["bloque"]
	senadorInfo["distrito"] = senador["distrito"]
	senadorInfo["nombre"] = senador["nombre"]
	return senadorInfo


def parse(soup):
	candidate = {}
	div = soup.find_all("div", class_= "col-md-4")[2]
	pTagSize = len(div.find_all("p"))
	candidate["mandato"] = "" if pTagSize < 5 else div.find_all("p")[4].text.split(":")[1].strip()
	return candidate


if __name__ == "__main__":
    main()
