import xml.etree.ElementTree as ET


def main():
	candidateSurname = "Gorbea"
	tree = ET.parse('GetDiputadosActivosNuevo.xml')
	historicalCandidate = findHistoricalCandidate(tree.getroot(),candidateSurname)
	print historicalCandidate
	



def findHistoricalCandidate(root, surname):
	results = []
	for child in root:
		if(child[0].text.lower() == surname.lower()):
			data = {}
			data["apellido"] = child[0].text
			data["nombre"] = str(child[1].text
			data["idLegislador"] = child[6].text
			data["fechaInicioMandato"] = child[9].text
			data["fechaFinMandato"] = child[10].text
			data["foto"] = child[14].text
			data["cargo"] = child[23].text
			results.append(data)

	if(len(results) > 1) :
		print "more than one result for historical candidates {}".format(results)
	if(len(results) == 0) :
		return {}

	return results[0]


if __name__ == "__main__":
    main()
