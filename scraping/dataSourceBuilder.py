import json
import base64
import requests
import io
import unicodedata
from modules import matcher
import xml.etree.ElementTree as ET

def main():
	boletas = readJsonFile('sources/boletas.json')
	source = {}
	source["diputados"] = readJsonFile('sources/diputados.json')
	source["senadores"] = readJsonFile('sources/senadores.json')
	source["twitters"] = readJsonFile('sources/twitters.json')
	source["legislaturaPorteniaActivos"] = readJsonFile('sources/legislaturaPorteniaActivos.json')
	source["legislaturaPorteniaHistoricos"] = readJsonFile('sources/legislaturaPorteniaHistoricos.json')
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
		results = results + findInDiputados(candidate, source["diputados"]) + findInSenadores(candidate, source["senadores"]) + findInTwitters(candidate, source["twitters"]) + findInLegislaguraPorteniaActivos(candidate, source["legislaturaPorteniaActivos"]) + findInLegislaguraPorteniaHistoricos(candidate, source["legislaturaPorteniaHistoricos"])
	return results	

def findInDiputados(candidate, sources):
	results = []
	for diputado in sources:		
		if(matcher.match(candidate, diputado)):
			diputado["imgAsb64"] = getImgAsBase64(diputado["img"])
			results.append(diputado)
	return results

def findInSenadores(candidate, sources):
	results = []
	for senador in sources:		
		if(matcher.match(candidate, senador)):
			senador["imgAsb64"] = getImgAsBase64(senador["img"])
			results.append(senador)
	return results

def findInTwitters(candidate, sources):
	results = []
	for twitter in sources:		
		if(matcher.match(candidate, twitter)):
			twitter["imgAsb64"] = getImgAsBase64(twitter["img"])
			results.append(twitter)
	return results

def findInLegislaguraPorteniaActivos(candidate, sources):
	results = []
	for legisladorPortenio in sources:		
		if(matcher.match(candidate, legisladorPortenio)):
			legisladorPortenio["imgAsb64"] = getImgAsBase64(legisladorPortenio["img"])
			results.append(legisladorPortenio)
	return results

def findInLegislaguraPorteniaHistoricos(candidate, sources):
	results = []
	for legisladorPortenio in sources:		
		if(matcher.match(candidate, legisladorPortenio)):
			legisladorHistorico = findInfo(legisladorPortenio["id_legislador"])
			#legisladorPortenio["imgAsb64"] = getImgAsBase64(legisladorPortenio["img"])
			results.append(legisladorHistorico)
	return results

def getImgAsBase64(url):
	return base64.b64encode(requests.get(url).content)

def findInfo(legisladorId):
	content = makeRequest(legisladorId)
	root = ET.fromstring(content)
	candidate = root[0]
	data = {}
	data["apellido"] = candidate[0].text
	data["nombre"] = candidate[1].text
	data["id_legislador"] = candidate[6].text
	data["fecha_inicio_mandato"] = candidate[9].text
	data["fecha_fin_mandato"] = candidate[10].text
	data["cantidad_exptes_autor"] = candidate[33].text 
	data["cantidad_exptes_coautor"] = candidate[34].text 
	data["cantidad_mandatos"] = candidate[35].text 
	return data

def makeRequest(legisladorId):
	payload = "id_legislador={}".format(legisladorId)
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r = requests.post("https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosyCargosActivosPorId_Legislador", payload, headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')

def readJsonFile(name):
	f = io.open(name, 'r', encoding='utf-8')
	data = json.load(f)
	f.close()
	return data

if __name__ == "__main__":
    main()