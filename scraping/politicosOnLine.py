from bs4 import BeautifulSoup

import requests
import json

def main():
	soup = get_content("http://www.politicosonline.com/ranking")
	paginationNumbers = get_pagination_numbers(soup)
	candidates = parse_candidates(soup)	

	for number in paginationNumbers:
		url = "http://www.politicosonline.com/ranking?desde={}&orderby=klout".format(int(number) - 1)
		print url
		candidates.extend(parse_candidates(get_content(url)))

	with open('data.json', 'w') as outfile:
	    json.dump(candidates, outfile, ensure_ascii=False)


def parse_candidates(soup):
	contents = soup.find(id="klout-top").find_all("tr")
	candidates = []
	for tr in contents[1: len(contents)]:
		tds = tr.find_all("td")
		data = {}
		data['img'] = tr.find_all("td")[0].contents[0]["src"]
		data['name'] = tr.find_all("td")[3].contents[0].text.encode('utf-8')
		data['href'] = tr.find_all("td")[3].contents[0]["href"]
		data['amountOfFollowers'] = tr.find_all("td")[5].text.encode('utf-8')
		data['description'] = str(tr.find_all("td")[6].text.encode('utf-8'))
		candidates.append(data)
	return candidates

def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	data = r.text.encode('utf-8')
	return BeautifulSoup(data, 'html.parser')

def get_pagination_numbers(soup):
	paginationBlock = soup.find(id="pagination-digg").find_all("a")
	def paginationNumbers(x): return str(x.text)
	return map(paginationNumbers, paginationBlock[0:5])

if __name__ == "__main__":
    main()


#http://www.politicosonline.com/ranking?desde=250&orderby=klout
#sudo apt-get install python-pip
#sudo pip install beautifulsoup4
#http://pbs.twimg.com/profile_images/653558348273569792/joxg8DZD_normal.png
#http://pbs.twimg.com/profile_images/653558348273569792/joxg8DZD.png
