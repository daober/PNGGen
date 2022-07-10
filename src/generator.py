from typing import List, BinaryIO, Tuple
from enum import Enum
import zlib
import struct
import os

Pixel = Tuple[int, int, int]

HEADER = b'\x89PNG\r\n\x1A\n'          # 4-byte length field; 4-byte chunk type field; data, 4-byte checksum
BLACK_PIXEL: Pixel = (0, 0, 0)
WHITE_PIXEL: Pixel = (255,255,255)

#from PNG SPEC
#NOTE: only 'TRUECOLOUR' && 'TRUECOLOUR_WITH_ALPHA' important for now
class PNGType(Enum):
    GREYSCALE = 0
    TRUECOLOUR = 2
    INDEXED_COLOUR = 3
    GREYSCALE_WITH_ALPHA = 4
    TRUECOLOUR_WITH_ALPHA = 6

Image = List[List[Pixel]]
#--------------------------------------------------------------

class PNGGenerator(object):
    def __init__(self):
        print("generating...")

    @classmethod
    def _get_checksum(cls, chunk_type: bytes, data: bytes) -> int:
        checksum = zlib.crc32(chunk_type)
        checksum = zlib.crc32(data, checksum)
        return checksum

    @classmethod
    def _chunk(cls, out: BinaryIO, chunk_type: bytes, data: bytes) -> None:
        out.write(struct.pack('>I', len(data)))                #endianess '>I' indicates a 4-byte big endian unsigned integer
        out.write(chunk_type)
        out.write(data)

        checksum = cls._get_checksum(chunk_type, data)
        out.write(struct.pack('>I', checksum))                 #endianess '>I' indicates a 4-byte big endian unsigned integer

    @classmethod
    def _make_ihdr(cls, width: int, height: int, bit_depth: int, color_type: int) -> bytes:
        return struct.pack('>2I5B', width, height, bit_depth, color_type, 0, 0, 0)

    @classmethod
    def _encode_data(cls, image: Image) -> List[int]:
        ret = []
        for row in image:
            ret.append(0)

            color_values = [
                color_value for pixel in row for color_value in pixel
            ]
            ret.extend(color_values)
        return ret

    @classmethod
    def _compress_data(cls, data: List[int]) -> bytes:
        data_bytes = bytearray(data)
        return zlib.compress(data_bytes)


    @classmethod
    def _make_idat(cls, image: Image) -> bytes:
        encoded_data = cls._encode_data(image)
        compressed_data = cls._compress_data(encoded_data)
        return compressed_data

    @classmethod
    def _write_png(cls, out: BinaryIO, png_type: PNGType, image: Image) -> None:
        out.write(HEADER) #write the header first

        assert len(image) > 0
        width = len(image[0])
        height = len(image)
        bit_depth = 8                # bits per pixel
        color_type = png_type.value

        ihdr_data = cls._make_ihdr(width, height, bit_depth, color_type)
        cls._chunk(out, b'IHDR', ihdr_data)
        compressed_data = cls._make_idat(image)
        cls._chunk(out, b'IDAT', data=compressed_data)
        cls._chunk(out, b'IEND', data=b'')

    @classmethod
    def save_png(cls, image: Image, png_type : PNGType, filepath: str) -> int:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        try:
            with open(filepath, 'wb') as out:                   #binary write operation is important!
                cls._write_png(out, png_type, image)
                print("generation of " + filepath + " done")
                return 0
        except IOError as error:
            print(error)
            return 1

    @classmethod
    def generate_checkerboard_imagedata(cls, width: int, height: int, cell_size: int = 10) -> Image:
        image = []
        length_one_square = height / cell_size
        length_two_squares = height / cell_size * 2

        for i in range(height):
            row = []
            if (i % length_two_squares) >= length_one_square:
                for j in range(width):
                    if (j % length_two_squares) < length_one_square:
                        row.append(WHITE_PIXEL)
                    else:
                        row.append(BLACK_PIXEL)
            else:
                for j in range(width):
                    if ( j % length_two_squares) >= length_one_square:
                        row.append(WHITE_PIXEL)
                    else:
                        row.append(BLACK_PIXEL)
            image.append(row)
        return image