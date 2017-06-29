from modules import request
from modules import files
import urllib

def main():
    soup = request.get_content_parsed("https://duckduckgo.com/html/?q=liliana+fadul+tierra+del+fuego")
    files.save_as_json_2('sources/resultsGoGoDuck.json', parse_results(soup))

def parse_results(soup):
    resultsBlocks = soup.find_all("div", attrs={"class":"links_main links_deep result__body"})
    results = []
    for resultDiv in resultsBlocks:
        data = {}
        url = resultDiv.find("a", attrs={"class":"result__a"})["href"]
        data["url"] = urllib.unquote(url.split("uddg=")[1])
        data["description"] = resultDiv.find("a", attrs={"class":"result__snippet"}).text
        results.append(data)
    return results

if __name__ == "__main__":
    main()