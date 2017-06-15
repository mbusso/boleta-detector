import json

def save_as_json(path, data):
	with open(path, 'w') as outfile:
	    json.dump(data, outfile, ensure_ascii=False)