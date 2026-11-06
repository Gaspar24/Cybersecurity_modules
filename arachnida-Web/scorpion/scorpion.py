#!/usr/bin/env python3

import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("path",type=str,nargs="*")
	args = parser.parse_args()
	if len(args.path) > 0:
		return args.path
	else:
		sys.exit("Nee to provide a path!")

def get_data_from_image(path):
	image = Image.open(path)
	exifdata = image.getexif()
	for tag_id, value in exifdata.items():
		tag_name = TAGS.get(tag_id,tag_id)
		print(f"{tag_name}: {value}")
		
def scorpion(arr_path):
	for path in arr_path:
		get_data_from_image(path)


def main():
	arr_path = parse_args()
	scorpion(arr_path)
if __name__ == "__main__":
	main()