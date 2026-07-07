#!/usr/bin/env python3 

import sys
import os
import requests
import re


def get_image_names():
	pass

def search_images(url):
	html = requests.get(url).text

	# print(html)
	if re.search(r"<img",html,re.I):
		print("Images found on site")
		# get_image_names()
	else:
		print("No immage found")


def spider():
	if len(sys.argv) > 1:
		url = sys.argv[1]
		search_images(url)
		


if __name__ == "__main__":
	spider()
