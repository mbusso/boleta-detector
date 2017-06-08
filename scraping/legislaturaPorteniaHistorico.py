import xml.etree.ElementTree as ET
import unicodedata
import requests
import json

def main():
	data = makeHistoricoRequest('http://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosHistorico')
	candidates = parseHistoricalCandidates(ET.fromstring(data))
	with open('sources/legislaturaPorteniaHistoricos.json', 'w') as outfile:
	    json.dump(candidates, outfile, ensure_ascii=False)

def parseHistoricalCandidates(root):
	results = []
	for child in root:
			data = {}
			data["id_legislador"] = child[0].text.encode('utf-8')
			data["apellido"] = child[1].text.encode('utf-8')
			if(child[2].text ): 
				data["nombre"] = child[2].text.encode('utf-8')
			else:
				data["nombre"] = ""
			data["id_autor"] = child[4].text.encode('utf-8')
			data["cantidad_mandatos"] = child[7].text.encode('utf-8')
			results.append(data)

	return results

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

def makeHistoricoRequest(url):
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r  = requests.post(url,"id_bloque=", headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')
	

def makeRequest(legisladorId):
	payload = "id_legislador={}".format(legisladorId)
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r = requests.post("https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosyCargosActivosPorId_Legislador", payload, headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')

if __name__ == "__main__":
    main()
