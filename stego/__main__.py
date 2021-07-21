
# runable module,

import os
import sys
import logging
import pathlib, importlib
from PIL import Image
from .common import _validate_passwd, images

parent = os.path.split(os.path.relpath(__file__))[0]

logging.basicConfig(format='%(message)s', level=logging.INFO)
logging.getLogger('PIL').setLevel(logging.WARNING)
logger = logging.getLogger('stego')

try:
	from PIL import UnidentifiedImageError
except:
	UnidentifiedImageError = OSError

def main(args):
	if args.verbose:
		logger.setLevel(logging.DEBUG)
	
	if args.quiet:
		logger.setLevel(logging.WARNING)

	if(args.info):
		run(args.image, args.file, ps='i')

	elif(args.remove):
		run(args.image, ps='r')

	elif(args.embed):
		if(args.message and args.embed and args.file == None):
			run(args.image, source=args.message ,password=args.password, ps='e')
		elif(args.file and args.embed and args.message == None):
			run(args.image, source=args.file ,password=args.password, ps='e')

	elif(args.extract):
		run(args.image, source=None ,password=args.password, ps='x')
	
	else:
		print('Insufficient data')

def run(image, source=None, password=None, ps='e'):
	'''Dynamically import modules and execute the desired operations.'''
	if not image.is_file():
		raise FileNotFoundError(f'{image}: File not found')
	try:
		imageobj = Image.open(str(image.joinpath()))

		if not imageobj.format.upper() in images:
			raise UnidentifiedImageError('Note: "%s" image format not supported by this project, either use PNG (recommended), TIFF, BMP or PPM image formats.' % (imageobj.format.upper()))
		
		password = _validate_passwd(password)

		if(ps == 'e'):
			if(isinstance(source, str)): # if message as input source
				source = source.encode('utf-8')
			encoder = importlib.import_module(parent+'.encoder')
			encoder.embed(
				imageobj = imageobj, source = source, 
				password = password,
				fileobj = isinstance(source, pathlib.Path)
			)
		
		elif(ps == 'x'):
			decoder = importlib.import_module(parent+'.decoder')
			decoder.extract(
				imageobj = imageobj, 
				password = password
			)
	
		elif(ps == 'r'):
			eraser = importlib.import_module(parent+'.eraser')
			eraser.clean(
				imageobj = imageobj
			)

		elif(ps == 'i'):
			base = importlib.import_module(parent+'.base')
			base.display_info(imageobj)
	
	except UnicodeDecodeError as error:
		logger.warn('Oops!, Invalid Password')

	except Exception as error:
		logger.warn('%s' % error)

	finally:
		if locals().get('imageobj'):
			locals().get('imageobj').close()

if __name__ == '__main__':
	from .cli import parse_args
	main(parse_args())