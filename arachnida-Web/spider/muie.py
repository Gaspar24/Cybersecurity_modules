#!/usr/bin/env python3 

import argparse
import sys
import os
import requests

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


def main():
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
	make_path(path)
	try:
		html_content = requests.get(url,timeout=3).text
	except:
		sys.exit("Error fetching the url :{url}")




if __name__ == "__main__":
	main()
