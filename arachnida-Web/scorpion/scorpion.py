#!/usr/bin/env python3

import os
import sys
import argparse
from PIL import Image
from PIL.ExifTags import TAGS


def print_banner():
    print("""
   ____  ____ ___  ____  ____  ____ ___  _   _
  / ___|/ ___/ _ \\|  _ \\|  _ \\|  _ \\_ _|| \\ | |
  \\___ \\ |  | | | | |_) | |_) | |_) | | |  \\| |
   ___) | |__| |_| |  _ <|  __/|  __/| | | |\\  |
  |____/ \\____\\___/|_| \\_\\_|   |_|  |___||_| \\_|

        [ IMAGE METADATA ANALYZER ]
    """)


def print_file_info(path, image):
	print("\n================================")
	print(f" FILE       : {path}")
	print(f" FORMAT     : {image.format}")
	print(f" RESOLUTION : {image.width} x {image.height}")
	print(f" MODE       : {image.mode}")
	print("================================")

def print_finished():
    print("\n[OK] ANALYSIS COMPLETED\n")

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("path",type=str,nargs="*") # + also works
	args = parser.parse_args()
	if len(args.path) > 0:
		return args.path
	else:
		sys.exit("Nee to provide a path!")

def get_basic_info(image,path):
	print("\n================================")
	print(f" FILE       : {path}")
	print(f" FORMAT     : {image.format}")
	print(f" RESOLUTION : {image.width} x {image.height}")
	print(f" MODE       : {image.mode}")
	print("================================")
	

def get_data_from_image(path):
	try:
		image = Image.open(path)
		get_basic_info(image,path)
		exifdata = image.getexif()
		if(len(exifdata) > 0):
			print("\n-------- EXIF METADATA --------")
			for tag_id, value in exifdata.items():
				tag_name = TAGS.get(tag_id,tag_id)
				print(f"{tag_name}: {value}")
			print("\n")
		else:
			print(f"No exif data found in {path}")
	except(OSError, ValueError) as e:
		print(f"Can not read {path} : {e}")
		
def scorpion(arr_path):
	for path in arr_path:
		get_data_from_image(path)


def main():
	print_banner()
	arr_path = parse_args()
	scorpion(arr_path)
	print_finished()

if __name__ == "__main__":
	main()