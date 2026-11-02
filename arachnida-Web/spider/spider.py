#!/usr/bin/env python3 

import argparse
import sys
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def parse_args():
	parser = argparse.ArgumentParser(description="Spider")
	parser.add_argument("-r", action="store_true", help="Recursively download images")
	parser.add_argument("-l", type=int, default=5, help="Maximum recursion depth (default: 5)")
	parser.add_argument("-p", type=str, default="./data/", help="Output folder (default: ./data/)")
	parser.add_argument("url", type=str, help="Target URL")
	args = parser.parse_args()
	if args.l < 0:
		parser.error("depth level (-l) must be a positive integer.")
	if not args.r:
		args.l = 0
	return args

def make_path(path):
	os.makedirs(path,exist_ok=True)

def get_images(html_content, url, path):
	soup = BeautifulSoup(html_content,"html.parser")
	img_tags = soup.find_all("img")
	for tag in img_tags:
		src = tag.get("src")
		# if not src or src.startswith("data:"):
		# 	continue
		img_url = urljoin(url,src)
		parsed_url = urlparse(img_url)
		clean_path = parsed_url.path
		if not clean_path.lower().endswith(VALID_EXTENSIONS):
			continue
		filename = os.path.basename(clean_path)
		if not filename:
			continue
		filepath = os.path.join(path, filename)
		try:
			response = requests.get(img_url, timeout=5)
			if response.status_code == 200:
				with open(filepath,"wb") as f:
					f.write(response.content)
		except:
			print(f"[-] Failed to download: {img_url}")

def get_links(html_content,base_url):
	arr_links = []
	soup = BeautifulSoup(html_content,"html.parser")
	for links in soup.find_all("a",href=True):
		link = links.get("href")
		arr_links.append(urljoin(base_url,link))
		# arr_links.append(link)
	return arr_links

def acces_url(url):
	try:
		html_content = requests.get(url,timeout=3).text

	except:
		sys.exit("Error fetching the url :{url}")
	return html_content


def spider():
	args = parse_args()
	if args.p:
		path = args.p
	else:
		path = "data"
	if args.l:
		depth = args.l
	else:
		depth = 5
	url = args.url
	html_content = acces_url(url)
	make_path(path)

	# while depth >= 0:

	get_images(html_content, url,path)
	arr_links = get_links(html_content,url)
	for link in arr_links:
		print(link)


def main():
	spider()


if __name__ == "__main__":
	main()

# https://www.magherallylens.com/simple-blogging-platforms/