from modules import request
from modules import files


def main():
	soup = request.get_content_parsed("http://www.legislaturadetucuman.gob.ar/infoseccion.php?seccion=0")
	candidates = parse(soup)
	files.save_as_json('sources/legisladoresTucuman.json', candidates)

def parse(soup):
	candidates = []
	contents = soup.find_all("div", attrs={"style": "clear:both; margin-bottom:10px;"})
	for child in contents:
		data = {}
		data["img"] = "http://www.legislaturadetucuman.gob.ar/" + child.find("img")["src"] 
		data["description"] = child.contents[1].text.encode('utf-8')
		name = child.contents[0].contents[0].encode('utf-8').split(",")
		data["nombre"] = name[1]
		data["apellido"] = name[0]
		data["partido"] = child.contents[0].find("span").text.encode('utf-8')
	 	candidates.append(data)
	return candidates


if __name__ == "__main__":
    main()
