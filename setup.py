#!/usr/bin/env python

from setuptools import setup

with open('README.md') as file:
	readme_content = file.read()

setup(
	author = "Smac01",
	name = "Stego",
	version = "1.0.1",
	description = "Steganography tool for embedding and extracting data.",
	long_description = readme_content,
	long_description_content_type = "text/markdown",
	url = "https://github.com/Smac01/Stego",
	license = "MIT",
	python_requires = ">=3.6",
	install_requires = [
		'Pillow>=5.1.0'
	]
)