#!/usr/bin/env python3

import unittest
import sys
sys.path.insert(0, '.')
from random import choice
from PIL import Image
from stego.eraser import clean
from stego.base import extract_metadata, make_array
from stego.common import get_header_info

images = ['test/rgba.png', 'test/cmyk.tiff', 'test/greyscale.bmp']

image = choice(images)

key = b'my_secret_key'

class SampleTestClean(unittest.TestCase):
	def test_cleanup(self):
		imageobj = Image.open(image)
		clean(imageobj)
		imageobj.close()
		imageobj = Image.open(image)
		array_1d = make_array(imageobj.getdata())
		exif = extract_metadata(array_1d)
		self.assertEqual(get_header_info(exif.typecode), None)

if __name__ == '__main__':
	unittest.main()