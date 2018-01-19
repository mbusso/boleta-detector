import requests
from bs4 import BeautifulSoup


def get_content(url):
	r  = requests.get(url)
	r.encoding = 'utf-8'
	return r.text.encode('utf-8')

def get_content_with_iso_enconding(url):
	r  = requests.get(url)
	r.encoding = 'iso-8859-1'
	return r.text.encode('iso-8859-1')


def get_content_parsed(url):
	data = get_content(url)
	return BeautifulSoup(data, 'html.parser')

def get_content_parsed_with_iso_encoding(url):
	data = get_content_with_iso_enconding(url)
	return BeautifulSoup(data, 'html.parser')

def parse(data):
	return BeautifulSoup(data, 'html.parser')

