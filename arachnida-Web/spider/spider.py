#!/usr/bin/env python3 

import argparse
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def print_banner():
    print("""
  ____  ____  ___ ____ _____ ____
 / ___||  _ \\|_ _|  _ \\ ____|  _ \\
 \\___ \\| |_) || || | | |  _| | |_) |
  ___) |  __/ | || |_| | |___|  _ <
 |____/|_|   |___|____/|_____|_| \\_\\

       [ WEB IMAGE CRAWLER ]
    """)


def print_status(url, depth, path):
	print("--------------------------------")
	print(f" TARGET : {url}")
	print(f" DEPTH  : {depth}")
	print(f" OUTPUT : {path}")
	print("--------------------------------")


def print_finished():
	print("\n--------------------------------")
	print("[OK] CRAWLING COMPLETED")
	print("--------------------------------")




def parse_args():
	parser = argparse.ArgumentParser(description="Spider")
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", type=int, default=5)
	parser.add_argument("-p", type=str, default="./data/")
	parser.add_argument("url", type=str)
	args = parser.parse_args()

	if args.l < 0:
		parser.error("Depth level must be a positive integer.")
	if not args.r:
		args.l = 0

	return args

def make_path(path):
	os.makedirs(path,exist_ok=True)


def get_unique_filepath(path, filename):
    name, ext = os.path.splitext(filename)
    filepath = os.path.join(path, filename)
    counter = 1
    while os.path.exists(filepath):
        new_filename = f"{name}_{counter}{ext}"
        filepath = os.path.join(path, new_filename)
        counter += 1
    return filepath

def get_images(html_content, url, path):
	soup = BeautifulSoup(html_content,"html.parser")
	img_tags = soup.find_all("img")
	for tag in img_tags:
		src = tag.get("src")
		if not src:
			continue
		img_url = urljoin(url,src)
		parsed_url = urlparse(img_url)
		clean_path = parsed_url.path
		if not clean_path.lower().endswith(VALID_EXTENSIONS):
			continue
		filename = os.path.basename(clean_path)
		if not filename:
			continue
		filepath = get_unique_filepath(path,filename)
		try:
			response = requests.get(img_url, timeout=5)
			response.raise_for_status()
			with open(filepath,"wb") as f:
				f.write(response.content)
		except requests.RequestException as e:
			print(f"Failed to download: {img_url}: {e}")

def get_links(html_content,base_url):
	arr_links = []
	soup = BeautifulSoup(html_content,"html.parser")
	for links in soup.find_all("a",href=True):
		base_link = links.get("href")
		full_link = urljoin(base_url, base_link)
		parsed_link = urlparse(full_link)
		if parsed_link.scheme in ("http","https"):
			arr_links.append(full_link)
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
	print_banner()
	
	args = parse_args()
	path = args.p
	depth = args.l
	url = args.url
	print_status(url,depth,path)
	visited_urls = set()
	make_path(path)
	spider(url,path,depth,visited_urls)
	print_finished()

if __name__ == "__main__":
	main()
