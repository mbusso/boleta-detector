from modules import request
from modules import files
from modules import repository
import urllib
import time

def main():
    initOutputFile(repository.findCandidatesWithoutResources())
    #levantar archivo
    #actualizar x registros con search results where "processed": false
    #guardar archivo

    #candidate = findCandidateResources("liliana", "fadul", "tierra del fuego")
    #results = []
    #results.append(candidate)
    #files.save_as_json_2('sources/resultsGoGoDuck.json', results)
    #time.sleep(5)   # delays for 5 seconds. You can Also Use Float Value.

def initOutputFile(candidates):
    if(files.exists('sources/resultsGoGoDuck.json')):
        print "File already exists"
    else:
        def createInitCandidate(candidate):
            data = {}
            print candidate
            data["nombre"] = candidate["nombre"]
            data["apellido"] = candidate["apellido"]
            data["processed"] = False
            return data

        results = map(lambda x: createInitCandidate(x), candidates)
        files.save_as_json_2('sources/resultsGoGoDuck.json', results)


def findCandidateResources(name, surname, province):
    nameFormatted = name.replace(" ", "+")
    surnameFormatted = surname.replace(" ", "+")
    provinceFormatted = province.replace(" ", "+")
    url = "https://duckduckgo.com/html/?q={}+{}+{}".format(nameFormatted, surnameFormatted, provinceFormatted)
    results = parse_results(request.get_content_parsed(url))
    candidate = {}
    candidate["nombre"] = name
    candidate["apellido"] = surname
    candidate["distrito"] = province
    candidate["url"] = url
    candidate["resources"] = results
    return candidate

def parse_results(soup):
    results = []
    resultsBlocks = soup.find_all("div", attrs={"class":"links_main links_deep result__body"})
    if(len(resultsBlocks) == 0):
        print soup
        return results
    else:    
        for resultDiv in resultsBlocks:
            data = {}
            url = resultDiv.find("a", attrs={"class":"result__a"})["href"]
            data["url"] = urllib.unquote(url.split("uddg=")[1])
            data["description"] = resultDiv.find("a", attrs={"class":"result__snippet"}).text
            results.append(data)
        return results

if __name__ == "__main__":
    main()