import sys
import os
from src.generator import PNGGenerator, PNGType

def main() -> int:

    image_data = PNGGenerator.generate_checkerboard_imagedata(1024, 768, 15)

    #GENERATE RGB PNG
    ret_code = PNGGenerator.save_png(image_data, PNGType.TRUECOLOUR, os.path.join('out', 'checkboard_example_rgb.png'))
    #GENERATE RGBA PNG
    ret_code = PNGGenerator.save_png(image_data, PNGType.TRUECOLOUR_WITH_ALPHA, os.path.join('out', 'checkboard_example_rgba.png'))
 
    return ret_code

if __name__ == '__main__':
    sys.exit(main())