import io
import requests
import json
import unicodedata

def main():
	data2017 = get_json("http://votaciones.lanacion.com.ar/api/diputados/ranking/2017?to_date=08-06-2017")
	data2016 = get_json("http://votaciones.lanacion.com.ar/api/diputados/ranking/2016")
	data2015 = get_json("http://votaciones.lanacion.com.ar/api/diputados/ranking/2015")
	data2014 = get_json("http://votaciones.lanacion.com.ar/api/diputados/ranking/2014")
	with io.open('sources/diputadosEstadisticas.json', 'w', encoding='utf-8') as outfile:
	    json.dump([data2017, data2016, data2015, data2014], outfile, ensure_ascii=False)
	

def get_json(url):
	data = get_content(url)
	return json.loads(data)

def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')


if __name__ == "__main__":
    main()	
