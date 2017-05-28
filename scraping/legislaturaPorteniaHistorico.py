import xml.etree.ElementTree as ET


def main():
	candidateSurname = "abbas"
	tree = ET.parse('GetDiputadosHistorico.xml')
	historicalCandidate = findHistoricalCandidate(tree.getroot(),candidateSurname)
	print historicalCandidate
	



def findHistoricalCandidate(root, surname):
	results = []
	for child in root:
		if(child[1].text.lower() == surname.lower()):
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


if __name__ == "__main__":
    main()
