from modules import request
from modules import files
from modules import repository
from modules import matcher
import urllib
import time

def main():
    initOutputFile(repository.findCandidatesWithoutResources())
    candidates = files.readJsonFile('sources/resultsGoGoDuck.json')
    processed = []
    for candidate in candidates:
        if((not candidate["processed"]) and (len(processed) <= 50)):
            result = findCandidateResources(matcher.normalize(candidate["nombre"]), matcher.normalize(candidate["apellido"]), matcher.normalize(candidate["distrito"]))
            candidate["resources"] = result["resources"]
            candidate["url"] = result["url"]
            candidate["processed"] = True
            processed.append(candidate)
            print "candidates processed {}".format(len(processed))
            time.sleep(10) # seconds
    files.save_as_json_2('sources/resultsGoGoDuck.json', candidates)        

def initOutputFile(candidates):
    if(files.exists('sources/resultsGoGoDuck.json')):
        print "File already exists"
    else:
        def createInitCandidate(candidate):
            data = {}
            data["nombre"] = candidate["nombre"]
            data["apellido"] = candidate["apellido"]
            data["distrito"] = candidate["distrito"]
            data["processed"] = False
            return data

        results = map(lambda x: createInitCandidate(x), candidates)
        files.save_as_json_2('sources/resultsGoGoDuck.json', results)


def findCandidateResources(name, surname, province):
    nameFormatted = name.replace(" ", "+")
    surnameFormatted = surname.replace(" ", "+")
    provinceFormatted = province.replace(" ", "+")
    url = "https://duckduckgo.com/html/?q={}+{}+{}".format(nameFormatted, surnameFormatted, provinceFormatted)
    results =  parse_results(request.get_content_parsed(url))
    searchedResult = {}
    searchedResult["url"] = url
    searchedResult["resources"] = results
    return searchedResult

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