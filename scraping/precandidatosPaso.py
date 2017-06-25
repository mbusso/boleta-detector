from modules import request
from modules import files
import json


def main():
	data = request.get_content("http://olcreativa.lanacion.com.ar/dev/get_url/?key2=1mIchf9frOP7w9IJfqIC7QJ28VB0SwwfAB2bJqP4AaBM&gid=0&output=json")
	files.save_as_json_2('sources/paso2017.json', json.loads(data))

if __name__ == "__main__":
    main()
