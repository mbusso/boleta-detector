import json
import io

def save_as_json(path, data):
	with open(path, 'w') as outfile:
	    json.dump(data, outfile, ensure_ascii=False)

def save_as_json_2(path, data):
	with io.open(path, 'w', encoding='utf-8') as outfile:
	    outfile.write(unicode(json.dumps(data, ensure_ascii=False)))

def readJsonFile(name):
	f = io.open(name, 'r', encoding='utf-8')
	data = json.load(f)
	f.close()
	return data	        