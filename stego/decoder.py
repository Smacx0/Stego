"""Extract data from images."""

from .base import (
	extract_metadata,
	make_array,
	as_string,
	extract_filename
)

from .common import (
	FILE, MESSAGE, PASSWORD,
	decode_stuffs,
	_get_passwd,
	get_header_info,
	as_bytes,
	IncorrectPassword
)

from .aes import aes_cbc_decrypt
import logging

logger = logging.getLogger('stego')

class HeaderNotFound(Exception):
	pass


def _decode_filename(password, filename):
	'''Decrypt the name of the file stored in lsb.'''	
	filename = aes_cbc_decrypt(key=password, data=filename)
	if not (filename and isinstance(filename, bytes)):
		raise ValueError('Oops!, Invalid Password')
	return filename[:-filename[-1]].decode()

@decode_stuffs
def _decompress(source, **kws):
	"""Convert compressed data to bytes and decrypt the data if encrypted."""
	try:
		return as_bytes(source)
	except:
		logger.warn('Oops, some data might have losted.')


def extract(imageobj, password=None):
	'''Extract data stored inside the image, making use of headers stored.'''
	img_data = make_array(imageobj.getdata())
	exif = extract_metadata(img_data)
	
	logger.debug(f'- {exif.size//8} bytes of data found to be stored in image lsb.')

	if (exif.typecode == MESSAGE) and exif.size > 0:
		# if message is stored without encryption
		content = as_string(img_data[slice(24, exif.size)])
		logger.info('\nMESSAGE:\n%s' % _decompress(content).decode('utf-8'))

	elif (exif.typecode == MESSAGE | PASSWORD) and exif.size > 0:
		# if message is stored with encryption
		if not password:
			password = _get_passwd()
		content = as_string(img_data[slice(24, exif.size)])
		logger.info('\nMESSAGE:\n%s' % _decompress(content, key=password).decode('utf-8'))

	elif(exif.typecode == FILE) and exif.size > 0:
		# if file is stored without encryption
		filename = extract_filename(img_data).decode()
		file_length = len(filename) * 8
		logger.info('+ extracting "%s"' % filename)
		logger.debug('"%s" file found to stored in image lsb of %d bytes.' % (filename, exif.size//8))
		content = as_string(img_data[slice(32+file_length, exif.size)])
		content = _decompress(content)
		with open(filename, 'wb') as file:
			file.write(content)
		logger.info('written to "%s"', filename)

	elif(exif.typecode == FILE | PASSWORD) and exif.size > 0:
		# if file is stored with encryption
		if not password:
			password  = _get_passwd()
		filename = extract_filename(img_data)
		file_length = len(filename) * 8
		filename = _decode_filename(password=password, filename=filename)
		if not filename:
			raise IncorrectPassword('Oops!, Invalid Password')
		logger.info('+ extracting "%s"' % filename)
		logger.debug('"%s" file found to stored in image lsb of %d bytes.' % (filename, exif.size//8))
		content = as_string(img_data[slice(32+file_length, exif.size)])
		content = _decompress(content, key=password)
		with open(filename, 'wb') as file:
			file.write(content)
		logger.info('written to "%s"', filename)

	else:
		raise HeaderNotFound("('-') Nothing interestingly found!!.")
