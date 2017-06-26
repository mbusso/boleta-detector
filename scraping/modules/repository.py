from modules import files
from modules import matcher
import xml.etree.ElementTree as ET
import base64
import requests

def findCandidates(candidates):
	source = __loadAllSources()
	matches = []
	notMatches = []

	for candidate in candidates:
		results = __findIn(candidate, source["diputados"]) + __findIn(candidate, source["senadores"]) + __findIn(candidate, source["twitters"]) + __findIn(candidate, source["legislaturaPorteniaActivos"]) + __findInLegislaguraPorteniaHistoricos(candidate, source["legislaturaPorteniaHistoricos"])
		if(len(results) > 0):
			matches = matches + results
		else:
			notMatches.append(candidate)

	data = {}
	data["matches"] = matches
	data["notMatches"] = notMatches
	return data

def __loadAllSources():
	source = {}
	source["diputados"] = files.readJsonFile('sources/diputados.json')
	source["senadores"] = files.readJsonFile('sources/senadores.json')
	source["twitters"] = files.readJsonFile('sources/twitters.json')
	source["legislaturaPorteniaActivos"] = files.readJsonFile('sources/legislaturaPorteniaActivos.json')
	source["legislaturaPorteniaHistoricos"] = files.readJsonFile('sources/legislaturaPorteniaHistoricos.json')
	return source;	

def __findIn(candidate, sources):
	results = []
	for data in sources:		
		if(matcher.match(candidate, data)):
			#candidate["imgAsb64"] = getImgAsBase64(candidate["img"])
			results.append(candidate)
	return results

def __findInLegislaguraPorteniaHistoricos(candidate, sources):
	results = []
	for legisladorPortenio in sources:		
		if(matcher.match(candidate, legisladorPortenio)):
			#legisladorHistorico = findInfo(legisladorPortenio["id_legislador"])
			#legisladorPortenio["imgAsb64"] = getImgAsBase64(legisladorPortenio["img"])
			#results.append(legisladorHistorico)
			results.append([])
	return results

def __getImgAsBase64(url):
	return base64.b64encode(requests.get(url).content)

def __findInfo(legisladorId):
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

def __makeRequest(legisladorId):
	payload = "id_legislador={}".format(legisladorId)
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r = requests.post("https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosyCargosActivosPorId_Legislador", payload, headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')	