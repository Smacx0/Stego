#!/usr/bin/env python3

import unittest

import sys
sys.path.insert(0, '.')

from random import choice
from PIL import Image
from stego.encoder import embed
from stego.decoder import extract, _decompress, IncorrectPassword
from stego.base import make_array, as_string, extract_metadata

images = ['test/rgba.png', 'test/cmyk.tiff', 'test/greyscale.bmp']

image = choice(images)

message = b'Pixels -> smallest unit(small colored square) that constitutes an images.'
key = b'my_secret_key'

def test_embed(message, password):
	imageobj = Image.open(image)
	embed(imageobj, message, password)

def test_extract(password):
	imageobj = Image.open(image)
	img_data = make_array(imageobj.getdata())
	exif = extract_metadata(img_data)
	content = as_string(img_data[slice(24, exif.size)])
	if password:
		content = _decompress(content, key=password)
	else:
		content = _decompress(content)

	return content

class SampleTestMessage(unittest.TestCase):

	def test_message(self):
		test_embed(message, None)
		content = test_extract(None)
		self.assertEqual(message, content)

	def test_message_with_encryption(self):
		test_embed(message,key)
		content = test_extract(key)
		self.assertEqual(message, content)
		self.assertRaises(IncorrectPassword,test_extract, b'random')

if __name__ == '__main__':
	unittest.main()