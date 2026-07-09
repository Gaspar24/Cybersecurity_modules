#!/usr/bin/env python3 

import sys
import os
import requests
import re
from urllib.parse import urljoin

def get_images(html_content):
	img_urls = re.findall(r'<img [^>]*src="([^"]+)"', html_content)
	try:
		for index in range(len(img_urls)):
			img_data = requests.get(img_urls[index]).content
			filepath = os.path.join("./data", f"test{index}")
			with open(filepath, "wb") as file:
				file.write(img_data)
	except:
		sys.exit("not working")


def get_links(html_content, base_url):
	raw_links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html_content)
	absolute_links = [urljoin(base_url, link) for link in raw_links]
	return absolute_links

def spider(url,depth):
	if depth <= 0:
		return
	
	try:
		os.makedirs("./data", exist_ok=True)
		html_content = requests.get(url,timeout=3).text
		get_images(html_content)
		links = get_links(html_content,url)

		for link in links:
			if link.startswith("http"):
				spider(link, depth - 1)

	except:
		sys.exit("Error fetching the url :{url}");


def main():
	depth = 3;
	if len(sys.argv) <= 1:
		sys.exit("Wrong number of args");
	url = sys.argv[1]
	spider(url,depth)
		


if __name__ == "__main__":
	main()
