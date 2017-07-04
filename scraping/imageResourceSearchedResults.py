from modules import files
from modules import matcher

def main():
    results = files.readJsonFile('sources/cleanedResultsGoGoDuck.json')
    cleanedResults = map(cleanResult, results)
    files.save_as_json_2('sources/cleanedResultsGoGoDuck.json', cleanedResults)	

def cleanResult(result):
    filtered = filter(twitterResources(), result["resources"])
    if(len(filtered) > 0):
        result["imageResource"] = filtered[0]        
    return result

def twitterResources():
    keywords = ["APYME","ANSES","ANMaC","Radical","Ministerio","Gabinete","Senado","Politica",
    "Sindicalismo","SUTEBA","izquierdasocialista.org.ar","izquierda","Diputada","Precandidata",
    "Militante","Senadora","Senador","Diputado","funcionario","mesas","empresario","dirigente",
    "militante","partido","obrero","provincial","Docentes","Sec","Legisladora","Legislador",
    "Legisladores","candidato","candidata","vicegobernador","diputados", "ministro","Presidenta",
    "peronista","concejo","consejo","deliberante","intendente","pte","concejal","intendenta","macri",
    "lista","directora","responsable","CFK","UCR","politico","social","desarrollo"]
    def twitter(resource):
        if("twitter.com" in resource["url"]):
            description = matcher.normalize(resource["description"])
            match = any(matcher.normalize(word) in description for word in keywords)
            if(not match):
                print resource["description"]
            return match
        else:
            return ""    
    return twitter

if __name__ == "__main__":
    main()
