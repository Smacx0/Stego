"""Cleanup data stored in images."""

from .common import (
	get_header_info
)

from .base import (
	extract_metadata,
	make_array,
	random_lsb
)

import logging
logger = logging.getLogger('stego')

def clean(imageobj):
	'''Remove the data stored in image lsb by the randomizing the bit.'''
	img_data = imageobj.getdata()
	
	if isinstance(img_data[0], int):
		num_channels = 1
	else:
		num_channels = len(img_data[0])
	
	img_data = make_array(img_data)

	exif = extract_metadata(img_data)
	
	if get_header_info(exif.typecode):
	
		logger.debug(f'Image Color type : {imageobj.mode}')

		# initializing pixel positions
		width = imageobj.size[0]
		x,y = 0, 0 

		for pixel in random_lsb(img_data, exif.size, num_channels):
			imageobj.putpixel((x,y), pixel)
			if(x == (width - 1 )):
				y += 1
				x = 0
			else:
				x += 1

		logger.debug(f'last pixel cleaned at position ({x},{y})')
		imageobj.save(imageobj.filename)
		imageobj.close()
		logger.info('+ cleaned up')
	else:
		logger.info("+ clean")
