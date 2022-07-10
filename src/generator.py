from typing import List, BinaryIO, Tuple
import zlib
import struct
import os

Pixel = Tuple[int, int, int]

HEADER = b'\x89PNG\r\n\x1A\n'          # 4-byte length field; 4-byte chunk type field; data, 4-byte checksum
BLACK_PIXEL: Pixel = (0, 0, 0)
WHITE_PIXEL: Pixel = (255,255,255)

Image = List[List[Pixel]]
#--------------------------------------------------------------

class PNGGenerator:
    def __init__(self):
        print("generating...")

    def _get_checksum(self, chunk_type: bytes, data: bytes) -> int:
        checksum = zlib.crc32(chunk_type)
        checksum = zlib.crc32(data, checksum)
        return checksum

    def _chunk(self, out: BinaryIO, chunk_type: bytes, data: bytes) -> None:
        out.write(struct.pack('>I', len(data)))                #endianess '>I' indicates a 4-byte big endian unsigned integer
        out.write(chunk_type)
        out.write(data)

        checksum = self._get_checksum(chunk_type, data)
        out.write(struct.pack('>I', checksum))                 #endianess '>I' indicates a 4-byte big endian unsigned integer

    def _make_ihdr(self, width: int, height: int, bit_depth: int, color_type: int) -> bytes:
        return struct.pack('>2I5B', width, height, bit_depth, color_type, 0, 0, 0)

    def _encode_data(self, image: Image) -> List[int]:
        ret = []

        for row in image:
            ret.append(0)

            color_values = [
                color_value for pixel in row for color_value in pixel
            ]
            ret.extend(color_values)
        return ret

    def _compress_data(self, data: List[int]) -> bytes:
        data_bytes = bytearray(data)
        return zlib.compress(data_bytes)

    def _make_idat(self, image: Image) -> bytes:
        encoded_data = self._encode_data(image)
        compressed_data = self._compress_data(encoded_data)
        return compressed_data

    def _write_png(self, out: BinaryIO, image: Image) -> None:
        out.write(HEADER) #write the header first

        assert len(image) > 0
        width = len(image[0])
        height = len(image)
        bit_depth = 8       # bits per pixel
        color_type = 2      # pixel is rgb triple

        ihdr_data = self._make_ihdr(width, height, bit_depth, color_type)
        self._chunk(out, b'IHDR', ihdr_data)
        compressed_data = self._make_idat(image)
        self._chunk(out, b'IDAT', data=compressed_data)
        self._chunk(out, b'IEND', data=b'')

    def save_png(self, image: Image, filepath: str) -> int:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        try:
            with open(filepath, 'wb') as out:                   #binary write operation is important!
                self._write_png(out, image)
                return 0
        except IOError as error:
            print(error)
            return 1

    def generate_checkerboard_imagedata(self, width: int, height: int, cell_size: int = 10) -> Image:
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