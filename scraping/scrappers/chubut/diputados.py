import sys
from os import path
sys.path.append( path.dirname(path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from modules import request
from modules import files

def main():
	soup = request.get_content_parsed("http://www.legischubut2.gov.ar/index.php?option=com_content&view=article&id=1254&Itemid=171")
	candidates = parse(soup)
	files.save_as_json('sources/chubut/diputados.json', candidates)

def parse(soup):
	candidates = []
	children = soup.find_all("div", attrs={"align":"center"})
	for child in children:
		data = {}
		data["img"] = child.contens[0]["src"]
		data["nombre"] = child.find("strong").text
		candidates.append(data)
	return candidates

if __name__ == "__main__":
	main()

