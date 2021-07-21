"""Emded data into images."""

from .base import (
	pixel_iterator,
	make_array
)

from .aes import aes_cbc_encrypt

from .common import (
	encode_stuffs,
	FILE, PASSWORD, MESSAGE, 
	HEADER, HEADER_LENGTH
)
import logging

logger = logging.getLogger('stego')

class EmbeddingDataBiggerThanImage(Exception):
	pass

def src_as_binary(source, size=8):
	"""Convert str/bytes object into 0's and 1's."""
	if isinstance(source, str):
		return [format(ord(char), f'0{size}b') for char in source]
	return [format(char, f'0{size}b') for char in source]

@encode_stuffs
def _compress(source, **kws) -> bytes:
	return source

def embed(imageobj, source, password=None, fileobj=False):
	'''Embed data into image lsb, supports compression and encryption.'''
	global HEADER, FILE, PASSWORD, HEADER_LENGTH

	if fileobj:
		# if file option is specified
		# converted to binary, encrypted if specified.
		filename = src_as_binary( 
			aes_cbc_encrypt(source.name.encode(), password) if password else source.name.encode('utf-8')
		)
		# compressed and converted to binary, encrypted if specified.
		file_source = src_as_binary(
			_compress(source.read_bytes(), key=password) if password else _compress(source.read_bytes())
		)
		fl = len(filename)	# length of the filename
		source = filename + file_source	
		del filename, file_source
	else:
		# if message option is specified
		# compressed and coverted to binary, encrypted if specified
		source = src_as_binary(
			_compress(source, key=password) if password else _compress(source)
		)

	source = ''.join(source)
	img_data = list(imageobj.getdata())

	# to determine pixel colors count
	if isinstance(img_data[0], int):
		num_channels = 1
	else:
		num_channels = len(img_data[0])
	
	image_bin_length = len(img_data)*num_channels	
	
	# +8 is added is file option is specified
	binary_length = (len(source) + HEADER_LENGTH) + 8 if fileobj else (len(source) + HEADER_LENGTH) # just for checking
	
	logger.debug(f'- Binary data size: {binary_length}, Image lsb size: {image_bin_length}')

	if(binary_length >= image_bin_length):
		raise EmbeddingDataBiggerThanImage('Caution: Source data bigger than image lsb')
	
	width = imageobj.size[0]
	x,y = 0, 0 # pixel location

	# generating headers based on user input
	if(fileobj and password):
		HEADER = FILE | PASSWORD
	elif (password and  not(fileobj)):
		HEADER = MESSAGE | PASSWORD
	elif (fileobj and not(password)):
		HEADER = FILE
	
	if fileobj:
		header_ = ''.join([format(HEADER, '08b'), format(binary_length//8, '016b'), format(fl, '08b')])
	else:
		header_ = ''.join([format(HEADER, '08b'), format(binary_length//8, '016b')])

	logger.debug(f'- {binary_length//8} bytes of data prepared to stored in image lsb')

	img_data = make_array(img_data)
	src_data = header_+source

	del header_, source

	for pixel in pixel_iterator(img_data, src_data, binary_length, num_channels):
		imageobj.putpixel((x,y), pixel)
		if(x == (width -1 )):
			y += 1
			x = 0
		else:
			x += 1

	logger.debug(f'- last pixel inserted at position ({x},{y})')
	imageobj.save(imageobj.filename)
	imageobj.close()
	logger.info('+ completed.')
