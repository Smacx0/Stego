"""Base functions for embed, extract and clean data."""

from collections import namedtuple
import array, random
from .common import (
	as_bytes,
	get_header_info,
	HEADER_LENGTH, 
	FILE
)

metadata = namedtuple('exif', 'typecode size')

def extract_metadata(img_data):
	'''Return metadata of the embedded data hidden inside the image lsb.'''
	return metadata(*extract_info(img_data))

def make_array(img_data):
	'''Convert image pixel to one dimensional array'''
	array_1d = array.array('B')
	for items in img_data:
		if isinstance(items, int):
			array_1d.append(items)
		else:
			for item in items:
				array_1d.append(item)
	return array_1d
 
def pixel_iterator(img_data, src_data, src_length, num_channels):
	'''Modify pixel lsb to store data and returns iterator of int/tuple based on color type.
	'''
	array_1d = array.array('B')
	for color, bit in zip(img_data, src_data):
		bit = int(bit)
		color = (color | bit) if bit else (color & ~1)
		array_1d.append(color)
	if num_channels > 1:
		return tuple(zip(*[iter(array_1d)]*num_channels))
	return array_1d

def random_lsb(img_data, src_length, num_channels):
	'''Randomize image pixel lsb to remove data.'''
	from random import random
	
	array_1d = array.array('B')
	for index in range(src_length):
		color = img_data[index] & ~1 if random() < 0.5 else img_data[index] | 1
		array_1d.append(color)
	if num_channels > 1:
		return tuple(zip(*[iter(array_1d)]*num_channels))
	return array_1d

def extract_info(img_data):
	'''Extract header info from image pixel lsb.'''
	header = as_string(img_data[slice(0,HEADER_LENGTH)])
	typecode, size = int(header[:8], 2), int(header[8: HEADER_LENGTH
		], 2) * 8
	return typecode, size

def as_string(img_data):
	'''Extract image pixel lsb.'''
	content = '';
	try:
		for j in img_data:
			if(j%2==0):
				content += '0'
			else:
				content += '1'
	except Exception as e:
		print(e)
	
	return content

def extract_filename(img_data):
	'''Extract filename stored in image pixel lsb.'''
	file_length = int(as_string(img_data[slice(24, 32)]),2)
	filename = as_string(img_data[slice(32, 32 + file_length * 8) ])
	return as_bytes(filename)

def display_info(imageobj):
	'''Display metadata of the image and data stored in lsb.'''
	array_1d = make_array(imageobj.getdata())
	exif = extract_metadata(array_1d)
	print('''Listing details:\n%-15s : %s\n%-15s : %s\n%-15s : %s\n%-15s : %dx%d\n%-15s : %s\n%-15s : %s''' % (
		'File name',imageobj.filename,\
		'File type', imageobj.format,\
		'Color type', imageobj.mode,\
		'Image size',imageobj.width, imageobj.height,\
		'Data stored', get_header_info(exif.typecode),\
		'Data size', f'{exif.size//8} bytes (gzip compressed)' if get_header_info(exif.typecode) else 0
	))
	if exif.typecode == FILE:
		filename = extract_filename(array_1d).decode()
		print('%-15s : %s' % ('++ file name', filename))
