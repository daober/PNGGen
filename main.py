import sys
import os
from src.generator import PNGGenerator

def main() -> int:
    generator = PNGGenerator()

    image_data = generator.generate_checkerboard_imagedata(1024, 768, 10)
    ret_code = generator.save_png(image_data, os.path.join('out', 'checkboard_example.png'))
    return ret_code

if __name__ == '__main__':
    sys.exit(main())