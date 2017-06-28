from modules import request
from modules import files


def main():
	soup = request.get_content_parsed("http://www.legislaturachaco.gov.ar/sitio/legisladores.php")
	candidates = parse(soup)
	files.save_as_json('sources/legisladoresChaco.json', candidates)

def parse(soup):
	candidates = []
	children = soup.find("div", class_="noticiascont").find_all("div", class_="row")	
	for i in range(2, len(children)):
	 	data = {}
	 	data["img"] = children[i].find("img")["src"].replace("..", "http://www.legislaturachaco.gov.ar")
	 	data["additionalInfo"] = children[i].find("a")["href"]
	 	name = children[i].find("a").text.encode('utf-8')
	 	data["apellido"] = children[i].find("a").contents[0].encode('utf-8').strip()
	 	data["nombre"] = children[i].find("a").contents[2].encode('utf-8').strip()
	 	data["partido"] = children[i].find_all("div", class_="tramitenom3")[1].text.encode('utf-8').strip()
	  	candidates.append(data)
	return candidates


if __name__ == "__main__":
    main()

