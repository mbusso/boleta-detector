from modules import request
from modules import files
import json


def main():
	data = request.get_content("http://olcreativa.lanacion.com.ar/dev/get_url/?key2=1mIchf9frOP7w9IJfqIC7QJ28VB0SwwfAB2bJqP4AaBM&gid=0&output=json")
	jsonOutput = process(data)
	files.save_as_json_2('sources/paso2017.json', jsonOutput)

def process(result):
	data = json.loads(result)
	for candidate in data:
		candidate["img"] = "http://especiales.lanacion.com.ar/multimedia/proyectos/17/elecciones/elecciones_2017_listas_confirmadas/img/" + candidate["img"]
	return data
if __name__ == "__main__":
    main()
