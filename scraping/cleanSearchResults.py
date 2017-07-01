from modules import files
from modules import matcher


def main():
    results = files.readJsonFile('sources/resultsGoGoDuck.json')
    cleanedResults = map(cleanResult, results)
    files.save_as_json_2('sources/cleanedResultsGoGoDuck.json', cleanedResults)

def cleanResult(result):
    result["resources"] = filter(cleanResources(matcher.normalize(result["nombre"]), matcher.normalize(result["apellido"])), result["resources"])
    return result

def cleanResources(nombre, apellido):
    def clean(resource):
        description = matcher.normalize(resource["description"])
        return (nombre in description) and (apellido in description)
    return clean


if __name__ == "__main__":
    main()    