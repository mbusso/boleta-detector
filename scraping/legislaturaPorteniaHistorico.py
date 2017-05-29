import xml.etree.ElementTree as ET
import unicodedata
import requests
import json

def main():
	candidateSurname = u"Sanchez Andia"
	tree = ET.parse('GetDiputadosHistorico.xml')
	historicalCandidate = findHistoricalCandidate(tree.getroot(),candidateSurname)
	if(historicalCandidate):
		print findInfo(historicalCandidate["id_legislador"])

def findHistoricalCandidate(root, surname):
	results = []
	for child in root:
		if(normalize(child[1].text) == normalize(surname)):
			data = {}
			data["id_legislador"] = child[0].text
			data["apellido"] = child[1].text
			data["nombre"] = child[2].text
			data["id_autor"] = child[4].text
			data["cantidad_mandatos"] = child[7].text
			results.append(data)

	if(len(results) > 1) :
		print "more than one result for historical candidates {}".format(results)
	if(len(results) == 0) :
		return {}

	return results[0]

def normalize(string):
	return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore').lower()


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

if __name__ == "__main__":
    main()
