import json
import io
import unicodedata
from modules import files
from modules import repository

def main():
	boletas = files.readJsonFile('sources/boletas.json')
	results = []	
	for boleta in boletas:
		boletaData = {}
		boletaData["boletaId"] = boleta["boletaId"]
		data = repository.findCandidates(boleta["candidatos"])
	  	boletaData["candidatos"] = data["matches"]
	  	boletaData["candidatosNotFound"] = data["notMatches"]
	  	results.append(boletaData)

	with io.open('sources/boletasOutput.json', 'w', encoding='utf-8') as outfile:
	    outfile.write(unicode(json.dumps(results, ensure_ascii=False, indent=4, sort_keys=True)))

if __name__ == "__main__":
    main()