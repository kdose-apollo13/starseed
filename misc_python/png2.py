"""
    +-----+
    !kDoSE¡
    +-----+

    endian -> big

----------------
MINIMAL PNG FILE
----------------

89 50 4E 47 0D 0A 1A 0A         PNG signature

00 00 00 0D                     data size 13 bytes
49 48 44 52                     IHDR
XX XX XX XX                     width               -|
XX XX XX XX                     height               |
XX                              bit depth            |
XX                              color type           | -- data
XX                              compression method   |
XX                              filter method        |
XX                              interlace method    -|
XX XX XX XX                     CRC (IHDR + data)

XX XX XX XX                     data size
49 44 41 54                     IDAT
ZZ ZZ ZZ ZZ ZZ ...              data *serialized*
XX XX XX XX                     CRC (IDAT + data)

[ optional multiple IDAT chunks ]

00 00 00 00                     data size
49 45 4E 44                     IEND
AE 42 60 82                     CRC (IEND)


------------------
SERIALIZE FOR IDAT
------------------

XX ...                          row of pixel data
00 XX ...                       prepend filter type None
00 XX ... 00 XX ...             concatenate all filtered rows
ZZ ZZ ZZ ZZ ZZ ...              zlib compress

"""

# companion to png.py

