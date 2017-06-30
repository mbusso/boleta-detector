import requests
from bs4 import BeautifulSoup


def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')


def get_content_parsed(url):
	data = get_content(url)
	return BeautifulSoup(data, 'html.parser')

def parse(data):
	return BeautifulSoup(data, 'html.parser')

