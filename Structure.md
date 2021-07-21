
### Structure

	+-----------------------------------------+
	|         HEADER (1 byte)                 |
	+-----------------------------------------+
	|          SIZE (2 bytes)                 |
	+-----------------------------------------+
	|     if MESSAGE; | if FILE;              |
	|       data      |   SIZE  (1 byte)      |
	|       EOF;      |   FILE NAME           |
	+-----------------------------------------+
	|            FILE data                    |
	|            EOF;                         |
	+-----------------------------------------+


Here is the structure, how the data is stored into the image lsb. Header section stores what kind of data is stored either message or file or encrypted data. Size section of the data stored including headers (in size of bytes). Other layers store the actual data.