import json
import base64
import requests
import io

def main():
	boletas = readJsonFile('sources/boletas.json')
	source = {}
	source["diputados"] = readJsonFile('sources/diputados.json')
	source["senadores"] = readJsonFile('sources/senadores.json')
	source["twitters"] = readJsonFile('sources/twitters.json')
	source["legislaturaPorteniaActivos"] = readJsonFile('sources/legislaturaPorteniaActivos.json')
	results = []	
	for boleta in boletas:
		boletaData = {}
		boletaData["boletaId"] = boleta["boletaId"]
	  	boletaData["candidatos"] = process(boleta, source)
	  	results.append(boletaData)

	with io.open('sources/boletaSource.json', 'w', encoding='utf-8') as outfile:
	    outfile.write(unicode(json.dumps(results, ensure_ascii=False)))

def process(boleta, source):
	results = []
	for candidate in boleta["candidatos"]:
		results = results + findInDiputados(candidate, source["diputados"]) + findInSenadores(candidate, source["senadores"]) + findInTwitters(candidate, source["twitters"]) + findInLegislaguraPortenia(candidate, source["legislaturaPorteniaActivos"])
	return results	

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
		if(candidate["apellido"] in twitter["nombre"]):
			twitter["imgAsb64"] = getImgAsBase64(twitter["img"])
			results.append(twitter)
	return results

def findInLegislaguraPortenia(candidate, sources):
	results = []
	for legisladorPortenio in sources:
		if(candidate["apellido"] in legisladorPortenio["apellido"]):
			legisladorPortenio["imgAsb64"] = getImgAsBase64(legisladorPortenio["img"])
			results.append(legisladorPortenio)
	return results

def getImgAsBase64(url):
	return base64.b64encode(requests.get(url).content)

def readJsonFile(name):
	f = io.open(name, 'r', encoding='utf-8')
	data = json.load(f)
	f.close()
	return data

if __name__ == "__main__":
    main()