import unicodedata

def match(candidate, source):
	if(__normalize(candidate["apellido"]) in __normalize(source["apellido"])):
		return __normalize(candidate["nombre"]) in __normalize(source["nombre"])
	else:
		return False		


def __normalize(string):
	return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore').lower()