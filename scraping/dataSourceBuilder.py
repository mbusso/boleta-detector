import json
import base64
import requests

def main():
	boletas = readJsonFile('boletas.json')
	source = {}
	source["diputados"] = readJsonFile('diputados.json')
	source["senadores"] = readJsonFile('senadores.json')
	source["twitters"] = readJsonFile('twitters.json')
	for boleta in boletas:
	  	process(boleta, source)
	    

def process(boleta, source):
	for candidate in boleta["candidatos"]:
		diputadoData = findInDiputados(candidate, source["diputados"])
		senadorData = findInSenadores(candidate, source["senadores"])
		twitterData = findInTwitters(candidate, source["twitters"])
		print twitterData

def findInDiputados(candidate, sources):
	results = []
	for diputado in sources:
		if(candidate["apellido"] == diputado["apellido"]):
			diputado["imgAsb64"] = getImgAsBase64(diputado["img"])
			results.append(diputado)
	return results

def findInSenadores(candidate, sources):
	results = []
	for senador in sources:
		if(candidate["apellido"] in senador["nombre"]):
			senador["imgAsb64"] = getImgAsBase64(senador["img"])
			results.append(senador)
	return results

def findInTwitters(candidate, sources):
	results = []
	for twitter in sources:
		if(candidate["apellido"] in twitter["name"]):
			twitter["imgAsb64"] = getImgAsBase64(twitter["img"])
			results.append(twitter)
	return results


def getImgAsBase64(url):
	return base64.b64encode(requests.get(url).content)

def readJsonFile(name):
	f = open(name, 'r') 
	data = json.load(f)
	f.close()
	return data

if __name__ == "__main__":
    main()