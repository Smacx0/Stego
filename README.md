
# Steganography

[![Python 3.x](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/smac01/Stego/master/LICENSE)

Stego uses least significant bit steganography to store a data in the image pixel. Currently this project make use of **Pillow** library provides support for PNG, TIFF, BMP or PPM (also related family) image formats and also provides support for all color types (RGB, RGBA, CMKY, GreyScale, ...) except binary images. In future versions, support for other image formats will also be added.

## Installation
You can download this project directly from github repository using command line:
```
git clone https://github.com/smac01/Stego.git
cd steganography
python3 setup.py install
```
You can also download as [zip](https://github.com/smac01/Stego/archive/main.zip).

## Usage
To get a list of all options and switches to use:
```bash
foo@bar:~$ python -m stego -h
```

### Embedding data
The following command used to store file data into the image. Also use **-p** options to password protect data, uses **AES** encryption.
```console
foo@bar:~$ python -m stego -e test/cmyk.tiff -f README.md
```

### Extracting data
The following command is used to extract data and write to file if file embedded else print message to console.
```console
foo@bar:~$ python -m stego -x test/cmyk.tiff
```

### Info 
Similar to *exiftool*, display metadata of the image file and data stored. 
```console
foo@bar:~$ python3 -m stego -i test/cmyk.tiff

Listing details:
File name       : test/cmyk.tiff
File type       : TIFF
Color type      : CMYK
Image size      : 120x120
Data stored     : FILE
Data size       : 1023 bytes (gzip compressed)
++ file name    : README.md
```

### Clean
Command used to remove the data present by randomizing the lsb of the image.
```console
foo@bar:~$ python -m stego -r test/cmyk.tiff
```

### Testing
```bash
foo@bar:~$ python test/test_message.py
foo@bar:~$ python test/test_file.py
foo@bar:~$ python test/test_clean.py
```
<div align="center">
	<ins>Suggestions are :heart: welcomed.</ins>
</div>