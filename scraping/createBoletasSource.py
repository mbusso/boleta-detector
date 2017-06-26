from modules import files
import re


def main():
	precandidates = files.readJsonFile('sources/paso2017.json')
	output = map(precandidates)
	files.save_as_json_2('sources/boletas.json', output)


def map(precandidates):
	result = {}
	for precandidate in precandidates:
		data = {}
		if(precandidate["apellido"].lower() != "definir"):
			data["partido"] = precandidate["nombre_partido"]
			data["nombre"] = re.sub(r'\d+-\s', '', precandidate["nombre"])
			data["apellido"] = precandidate["apellido"] 
			data["img"] = precandidate["img"]
			data["banca"] = precandidate["banca"]
			data["distrito"] = precandidate["distrito"]

			if(data["partido"] in result):
				result[data["partido"]].append(data)
			else :
				result[data["partido"]] = [data]

	output = []
	for key in result:
		data = {}
		data["boletaId"]= key
		data["candidatos"]= result[key]
		output.append(data)


	return output	


if __name__ == "__main__":
    main()
