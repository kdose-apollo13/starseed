""" +-----+ !kDoSE¡ +-----+
"""
from functools import partial
from zlib import compress, crc32


as_bytes = partial(int.to_bytes, length=4, byteorder='big')

PNG_signature = bytes.fromhex('89 50 4E 47 0D 0A 1A 0A')

IHDR_size = as_bytes(13)
IHDR = bytes.fromhex('49 48 44 52')
width = as_bytes(200)
height = as_bytes(100)
bit_depth = b'\x08'
color_type = b'\x00'  # 8-bit grayscale
compression = b'\x00'
filter_method = b'\x00'
interlace = b'\x00'
IHDR_data = b''.join((
    width, height, bit_depth, color_type,
    compression, filter_method, interlace
))
IHDR_CRC = as_bytes(crc32(IHDR + IHDR_data))

IDAT = bytes.fromhex('49 44 41 54')
pd = bytearray()  # pixel data
for _ in range(100):  # height
    pd.append(0x00)  # filter -> no transformation
    for p in range(200):  # width
        pd.append(0x97)  # pixel color
IDAT_data = compress(pd, level=9)
IDAT_size = as_bytes(len(IDAT_data))
IDAT_CRC = as_bytes(crc32(IDAT + IDAT_data))

IEND_size = as_bytes(0)
IEND = bytes.fromhex('49 45 4E 44')
IEND_CRC = as_bytes(crc32(IEND))

datastream = b''.join((
    PNG_signature,
    IHDR_size, IHDR, IHDR_data, IHDR_CRC,
    IDAT_size, IDAT, IDAT_data, IDAT_CRC,
    IEND_size, IEND, IEND_CRC
))

with open('gray.png', 'wb') as w:
    w.write(datastream)

