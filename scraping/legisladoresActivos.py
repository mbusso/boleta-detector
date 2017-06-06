import xml.etree.ElementTree as ET
import json
import requests


def main():
	data = makeRequest('http://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosActivosNuevo')
	candidates = parseData(ET.fromstring(data))
	with open('sources/legislaturaPorteniaActivos.json', 'w') as outfile:
	    json.dump(candidates, outfile, ensure_ascii=False)


def parseData(root):
	results = []
	for child in root:
		data = {}
		data["apellido"] = child[0].text.encode('utf-8')
		data["nombre"] = child[1].text.encode('utf-8')
		data["idLegislador"] = child[6].text.encode('utf-8')
		data["fechaInicioMandato"] = child[9].text.encode('utf-8')
		data["fechaFinMandato"] = child[10].text.encode('utf-8')
		data["foto"] = child[14].text.encode('utf-8')
		data["cargo"] = child[23].text
		results.append(data)
	return results	

def makeRequest(url):
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r  = requests.post(url,"id_bloque=", headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')

if __name__ == "__main__":
    main()
