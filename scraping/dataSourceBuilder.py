import json
import base64
import requests

def main():
	with open('boletas.json') as json_data:
	    boletas = json.load(json_data)
	    for boleta in boletas:
	    	process(boleta)
	    

def process(boleta):
	for candidate in boleta["candidatos"]:
		diputadoData = findInDiputados(candidate)
		senadorData = findInSenadores(candidate)

def findInDiputados(candidate):
	results = []
	with open('diputados.json') as diputados_data:
		diputados = json.load(diputados_data)
		for diputado in diputados:
			if(candidate["apellido"] == diputado["apellido"]):
				diputado["imgAsb64"] = getImgAsBase64(diputado["img"])
				results.append(diputado)
	return results

def findInSenadores(candidate):
	results = []
	with open('senadores.json') as senadores_data:
		senadores = json.load(senadores_data)
		for senador in senadores:
			if(candidate["apellido"] in senador["nombre"]):
				senador["imgAsb64"] = getImgAsBase64(senador["img"])
				results.append(senador)
	return results

def getImgAsBase64(url):
	return base64.b64encode(requests.get(url).content)

if __name__ == "__main__":
    main()