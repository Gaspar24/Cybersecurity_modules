#!/usr/bin/env python3 

import sys
import os
import requests
import re


def get_images(html_content):
	img_urls = re.findall(r'<img [^>]*src="([^"]+)"', html_content)
	try:
		img_data = requests.get(img_urls[1]).content
		filepath = os.path.join("./data", "test1")
		with open(filepath, "wb") as file:
			file.write(img_data)
	except:
		sys.exit("not working")

def spider(url):
	try:
		os.makedirs("./data", exist_ok=True)
		html_content = requests.get(url).text
		get_images(html_content)

	except:
		sys.exit("Error fetching the url :{url}");


def main():
	if len(sys.argv) <= 1:
		sys.exit("Wrong number of args");
	url = sys.argv[1]
	spider(url)
		


if __name__ == "__main__":
	main()
