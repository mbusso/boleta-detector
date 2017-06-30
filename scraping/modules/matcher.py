import unicodedata

def match(candidate, source):
	if(normalize(candidate["apellido"]) in normalize(source["apellido"])):
		return normalize(candidate["nombre"]) in normalize(source["nombre"])
	else:
		return False		


def normalize(string):
	return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore').lower()