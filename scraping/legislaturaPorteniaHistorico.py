import xml.etree.ElementTree as ET
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



def makeHistoricoRequest(url):
	headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
	r  = requests.post(url,"id_bloque=", headers=headers)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')
	

if __name__ == "__main__":
    main()
