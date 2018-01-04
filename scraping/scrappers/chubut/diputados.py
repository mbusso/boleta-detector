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
	bloque = ""
	children = soup.find_all("td")
	mandato = soup.find("h1", class_="title").contents[1].text.split(" ")[1]
	for child in children:
		strong = child.find("strong")
		if(strong):
			img = child.find("img")
			if(img):
				data = {}
				data["img"] = "http://www.legischubut2.gov.ar" + img["src"]
				data["nombre"] = strong.text.split("Dip.")[1].strip()
				data["bloque"] = bloque
				data["mandato"] = mandato
				candidates.append(data)
			else :
				tokens = strong.text.split("BLOQUE")
				if(len(tokens) > 1):
					bloque = tokens[1].split("Integrado")[0].strip()
	return candidates

if __name__ == "__main__":
	main()

