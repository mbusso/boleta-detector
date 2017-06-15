from modules import request
from modules import files


def main():
	soup = request.get_content_parsed("http://www.legiscba.gob.ar/legisladores/")
	candidates = parse(soup)
	files.save_as_json('sources/legisladoresCordoba.json', candidates)

def parse(soup):
	candidates = []
	contents = soup.find_all("div", class_="listados")
	a =  contents[0].contents[1]
	for child in contents:
		data = {}
		a =  child.contents[1]
		name = a.find("p").text.encode('utf-8').split(",")
		data["nombre"] = name[1]
		data["apellido"] = name[0]
		data["img"] = a.contents[1]["src"].replace("..","http://www.legiscba.gob.ar")
		data["additionalData"] = a["href"].replace("..","http://www.legiscba.gob.ar")
		candidates.append(data)
	return candidates


if __name__ == "__main__":
    main()
