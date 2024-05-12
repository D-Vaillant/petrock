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

    def test_basic_functionality_w_filepath(self):
        for img in self.test_imgs:
            rc = self.v.get_caption_from_image_path(img)
            with self.subTest(rc=rc):
                self.assertIsNotNone(rc)
        
    def test_classification(self):
        for i, img in enumerate(self.test_imgs):
            pattern = r'images/(\w+)\.jpg'
            label = re.search(pattern, img).group(1)
            response_caption = self.v.caption_image(Image.open(img))
            # Basically - check if it captions a cat image as 'cat' in some way.
            logging.info(f"LLM Response: {response_caption}")
            with self.subTest(label=label, response_caption=response_caption):
                self.assertIn(label, response_caption)


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