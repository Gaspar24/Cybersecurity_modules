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
	parser.add_argument("-r", action="store_true",
                        help="recursively download images")
	parser.add_argument("-l", type=int, default=5,
                        help="maximum recursion depth (default: 5)")
	parser.add_argument("-p", type=str, default="./data/",
                        help="output folder (default: ./data/)")
	parser.add_argument("url", type=str, help="Target URL")
	args = parser.parse_args()

	if args.l < 0:
		parser.error("Depth level must be a positive integer.")
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
			response.raise_for_status()
			with open(filepath,"wb") as f:
				f.write(response.content)
		except requests.RequestException as e:
			print(f"[-] Failed to download: {img_url}: {e}")

def get_links(html_content,base_url):
	arr_links = []
	soup = BeautifulSoup(html_content,"html.parser")
	for links in soup.find_all("a",href=True):
		base_link = links.get("href")
		full_link = urljoin(base_url, base_link)
		if full_link.startswith("http"):
			arr_links.append(urljoin(base_url,full_link))
	return arr_links

def acces_url(url):
	try:
		response = requests.get(url,timeout=3)
		response.raise_for_status()
		return response.text
	except requests.RequestException as e:
		print(f"Error fetching the url :{url} : {e}")
		return None


def spider(url,path,depth, visited_urls):
	if depth < 0:
		return
	if url in visited_urls:
		return
	visited_urls.add(url)

	html_content = acces_url(url)
	if html_content is None:
		return

	get_images(html_content, url,path)
	if depth == 0:
		return
	arr_links = get_links(html_content,url)
	for link in arr_links:
		spider(link,path,depth-1,visited_urls)

def main():
	args = parse_args()
	path = args.p
	depth = args.l
	url = args.url
	visited_urls = set()
	make_path(path)
	spider(url,path,depth,visited_urls)

if __name__ == "__main__":
	main()
