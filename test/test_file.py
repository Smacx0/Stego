#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0, '.')
from random import choice
from PIL import Image
from stego.encoder import embed
from stego.decoder import extract, _decompress, IncorrectPassword
from stego.base import make_array, as_string, extract_metadata

import os
import pathlib

images = ['test/rgba.png', 'test/cmyk.tiff', 'test/greyscale.bmp']

file = 'test/sample.txt'

image = choice(images)

key = b'my_secret_key'

def test_embed(message, password):
	imageobj = Image.open(image)
	embed(imageobj, message, password, True)
	imageobj.close()

def test_extract(password):
	imageobj = Image.open(image)
	extract(imageobj, password)
	imageobj.close()

class SampleTestFile(unittest.TestCase):

	def test_file(self):
		main_file = pathlib.Path(file)
		main_file_content = main_file.read_bytes()
		test_embed(main_file, None)
		test_extract(None)
		extract_file = pathlib.Path(file)
		extract_file_content = extract_file.read_bytes()
		os.remove('sample.txt')
		self.assertEqual(main_file_content, extract_file_content)

	def test_file_with_encryption(self):
		main_file = pathlib.Path(file)
		main_file_content = main_file.read_bytes()
		test_embed(main_file, key)
		# main_file.rename('main_file')
		test_extract(key)
		extract_file = pathlib.Path(file)
		extract_file_content = extract_file.read_bytes()
		os.remove('sample.txt')
		self.assertEqual(main_file_content, extract_file_content)
		self.assertRaises(IncorrectPassword,test_extract, b'random stuffs')

if __name__ == '__main__':
	unittest.main()