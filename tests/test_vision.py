import re
import logging
import unittest
from PIL import Image

from petrock.vision import Vision, OpenCVWebcam

TESTING_WEBCAM: bool = False


class TestCaptionImage(unittest.TestCase):
    test_imgs = ['images/cat.jpg', 'images/dog.jpg']

    def setUp(self):
        self.v = Vision()

    def test_classification(self):
        for img in self.test_imgs:
            pattern = r'images/(\w+)\.jpg'
            name = re.search(pattern, img).group(1)
            r = self.v.caption_image(Image.open(img))
            # Basically - check if it captions a cat image as 'cat' in some way.
            logging.info(f"LLM Response: {r}")
            self.assertIn(name, r)


@unittest.skipUnless(TESTING_WEBCAM, "Not testing webcam functionality.")
class TestRaspberryPiCamera(unittest.TestCase):
    def setUp(self):
        self.v = Vision(OpenCVWebcam())

    def test_image_capture(self):
        img = self.v.use_webcam()
        self.assertIsNotNone(img)


class TestRandomWebcam(unittest.TestCase):
    ...


if __name__ == "__main__":
    unittest.main()