import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files

def main():
	soup = request.get_content_parsed("http://www.senadodecatamarca.gob.ar/informacion-institucional/senadores")
	candidates = parse(soup)
	files.save_as_json('sources/catamarca/senadores.aux.json', candidates)

def parse(soup):
	candidates = []
	children = soup.find("table", class_="table table-striped table-bordered center-table").find("tbody").find_all("tr")
	for child in children:
		data = {}
		data["img"] = child.find("img")["src"]
		link = child.find("a")
		data["additionalInfo"] = link["href"]
		data["nombre"] = link.text.strip()
		tdElements = child.find_all("td")
		data["distrito"] = tdElements[1].text.strip()
		data["bloque"] = tdElements[2].text.strip()
		candidates.append(data)
	return candidates

if __name__ == "__main__":
	main()

