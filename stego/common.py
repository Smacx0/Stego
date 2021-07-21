"""Common attr/functions."""

import array, gzip
from .aes import aes_cbc_encrypt, aes_cbc_decrypt

MESSAGE :int 		= 0x01		# 1
FILE :int 			= 0x02		# 2
PASSWORD :int 		= 0x04		# 4
HEADER :int 		= MESSAGE 	# 1
HEADER_LENGTH :int 	= 0x18		# 24

GZIP_HEADER_HEX = b'\x1f\x8b'.hex()

headers = {1:'MESSAGE',2:'FILE', 5: 'ENCRYPTED', 6: 'ENCRYPTED'}
images = {'PNG', 'TIFF', 'BMP', 'PPM', 'PGM', 'PBM'}

class IncorrectPassword(Exception):
	pass

def as_bytes(source: str) -> bytes:
	'''Convert 0's and 1's to bytes'''
	bytes_data = array.array('B')
	for _ in range(0,len(source), 8):
		bytes_data.append(int(source[_:_+8], 2))
	return bytes_data.tobytes()

def get_header_info(header: int) -> str:
	'''Return type of data stored in image lsb based on header value.'''
	return headers.get(header, None)

def _validate_passwd(password: str) -> bytes:
	'''validate password to stick certain conditions'''
	if password and (len(password) < 8 or password.find(' ') > 0):
		raise ValueError('password must be min 8 characters lengths and spaces should not be used.')
	return password.encode() if password else None

def _get_passwd() -> bytes:
	"""Prompt for a password, with echo to console turned off."""
	import getpass
	password = getpass.getpass('Data is found to be password protected!!\nPlease enter password to proceed: ')
	return _validate_passwd(password)

def encode_stuffs(func=None) -> bytes:
	# decorator to compress and encrypt data
	original_func = func
	def run(*args, **kws):
		source = original_func(*args, **kws)
		source = gzip.compress(source)
		if('key') in kws.keys():
			source = aes_cbc_encrypt(key=kws['key'],data=source)
		return source + b'\x00'# just a temp byte
	return run

def decode_stuffs(func=None) -> bytes:
	# decorator to decrypt and decompress data
	original_func = func
	def run(*args, **kws):
		source = original_func(*args, **kws)
		source = source[:-1] # remove temp byte
		if('key') in kws.keys():
			source = aes_cbc_decrypt(key=kws['key'],data=source)
			pad = source[-1]
			if pad < 16 and source[-pad:] == bytes([pad]*pad):
				source = source[:-pad]
			if not (source or isinstance(source, bytes)) or source[:2].hex() != GZIP_HEADER_HEX:
				raise IncorrectPassword('Oops!, Invalid Password')
		source = gzip.decompress(source)
		return source 
	return run

