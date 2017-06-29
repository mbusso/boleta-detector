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
		diputados = __findIn(candidate, source["diputados"], "diputadosNacionales")
		senadores = __findIn(candidate, source["senadores"], "senadoresNacionales")
		twitters = __findIn(candidate, source["twitters"], "twitter")
		legisladoresPortenios = __findIn(candidate, source["legislaturaPorteniaActivos"],"legislaturaPortenia")
		legisladoresPorteniosHistoricos =  __findInLegislaguraPorteniaHistoricos(candidate, source["legislaturaPorteniaHistoricos"], "legislaturaPorteniaHistoricos")
		legisladoresChaco = __findIn(candidate, source["legisladoresChaco"], "legisladoresChaco")
		legisladoresTucuman = __findIn(candidate, source["legisladoresTucuman"], "legisladoresTucuman")
		legisladoresCordoba = __findIn(candidate, source["legisladoresCordoba"], "legisladoresCordoba")

		results =  sum([diputados, senadores, twitters, legisladoresPortenios, legisladoresPorteniosHistoricos, legisladoresChaco, legisladoresCordoba, legisladoresTucuman], [])
		if(len(results) > 0):
			matches = matches + results
		else:
			candidate["source"] = "empty"
			notMatches.append(candidate)

	data = {}
	data["matches"] = matches
	data["notMatches"] = notMatches
	return data

def findCandidatesWithoutResources():
	candidates = files.readJsonFile('sources/boletasOutput.json')
	return list(map(lambda c: c["candidatosNotFound"] , candidates))


def __loadAllSources():
	source = {}
	source["diputados"] = files.readJsonFile('sources/diputados.json')
	source["senadores"] = files.readJsonFile('sources/senadores.json')
	source["twitters"] = files.readJsonFile('sources/twitters.json')
	source["legislaturaPorteniaActivos"] = files.readJsonFile('sources/legislaturaPorteniaActivos.json')
	source["legislaturaPorteniaHistoricos"] = files.readJsonFile('sources/legislaturaPorteniaHistoricos.json')
	source["legisladoresChaco"] = files.readJsonFile('sources/legisladoresChaco.json')
	source["legisladoresTucuman"] = files.readJsonFile('sources/legisladoresTucuman.json')
	source["legisladoresCordoba"] = files.readJsonFile('sources/legisladoresCordoba.json')
	return source;	

def __findIn(candidate, sources, tag):
	results = []
	for data in sources:		
		if(matcher.match(candidate, data)):
			#candidate["imgAsb64"] = getImgAsBase64(candidate["img"])
			candidate["source"] = tag
			results.append(candidate)
	return results

def __findInLegislaguraPorteniaHistoricos(candidate, sources, tag):
	results = []
	for legisladorPortenio in sources:		
		if(matcher.match(candidate, legisladorPortenio)):
			#legisladorHistorico = findInfo(legisladorPortenio["id_legislador"])
			#legisladorPortenio["imgAsb64"] = getImgAsBase64(legisladorPortenio["img"])
			#results.append(legisladorHistorico)
			legisladorPortenio["source"] = tag
			results.append(legisladorPortenio)
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