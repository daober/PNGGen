import unittest
import os
from src.generator import PNGGenerator, PNGType


class GeneratorTest(unittest.TestCase):

    def setUp(self):
        self.filepath_rgb = os.path.join('test_out', 'checkboard_example_rgb.png')
        self.filepath_rgba = os.path.join('test_out', 'checkboard_example_rgba.png')

    def test_rgb_png(self):
        image_data = PNGGenerator.generate_checkerboard_imagedata(1024, 768, PNGType.TRUECOLOUR, 15)
        self.assertGreater(len(image_data), 0)
        self.assertEqual(0, PNGGenerator.save_png(image_data, PNGType.TRUECOLOUR, self.filepath_rgb))

    def test_rgba_png(self):
        image_data = PNGGenerator.generate_checkerboard_imagedata(1024, 768, PNGType.TRUECOLOUR_WITH_ALPHA, 15)
        self.assertGreater(len(image_data), 0)
        self.assertEqual(0, PNGGenerator.save_png(image_data, PNGType.TRUECOLOUR_WITH_ALPHA, self.filepath_rgba))
        
    def test_png_existence(self):
        self.assertTrue(os.path.isfile(self.filepath_rgb))
        self.assertTrue(os.path.isfile(self.filepath_rgba))

    def test_png_rgb_filled(self):
        self.assertGreater(os.path.getsize(self.filepath_rgba), 0)

    def test_png_rgba_filled(self):
        self.assertGreater(os.path.getsize(self.filepath_rgba), 0)

    