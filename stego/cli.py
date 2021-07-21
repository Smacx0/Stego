
from argparse import ArgumentParser, ArgumentTypeError
import pathlib

from . import __version__ as version

def validate_path(file: str) -> pathlib.Path:
	'''Validate file path provided'''
	path = pathlib.Path(file)
	if not path.exists():
		raise ArgumentTypeError("file does not exist.")
	
	if not path.is_file():
		raise ArgumentTypeError("not a file.")

	return path

def parse_args():
	parser = ArgumentParser(prog='stego', description='''
		Image steganography tool to embed and extract data. Currently support PNG, TIFF, BMP and PPM (and related family) image formats.
		''', epilog='''samples:
			%(prog)s -e image.png -f secret_file.txt 
		''')
	
	main_opt = parser.add_argument_group(title='the first argument must be one of the following flag arguments')
	main_opt.add_argument('image', help='image file for stego', type=validate_path )
	opt = main_opt.add_mutually_exclusive_group()
	opt.add_argument('-e','--embed', help='embed data into the image file (flag)', action='store_true')
	opt.add_argument('-x','--extract', help='extract data from the image file (flag)', action="store_true")
	opt.add_argument('-i','--info', help='list info about the image file (flag)', action='store_true')
	opt.add_argument('-r','--remove', help='remove the data stored in image file (flag)', action='store_true')

	parser.add_argument('-m','--message', help='embed string data into the image file', type=str, metavar='')
	parser.add_argument('-f','--file', help='file to be used', metavar='', type=validate_path)
	parser.add_argument('-p','--password', help='password protect the data', metavar='')
	parser.add_argument('-V','--version', help='version of the script', action='version', version=f'%(prog)s: {version}')
	parser.add_argument('-q','--quiet', help='quiet operation', action='store_true')
	parser.add_argument('-v','--verbose', help='be verbose', action='store_true')
	
	parser._action_groups.reverse() # reverse the parser args
	args = parser.parse_args()

	if not any([args.embed, args.extract, args.info, args.remove]):
		parser.error('Insufficient argument: required -e | -x | -i | -r')
	
	return args
