from PIL import Image


class Webcam:
    def get_image(self) -> Image:
        raise NotImplementedError("Webcam class must have `get_image()` implemented.")


class Vision:
    def __init__(self, device: Webcam=None):
        # device is some class that implements `get_image`
        # `get_image` should return a PIL image.
        if device is not None:
            self.device = device
    
    def process_webcam_input(raw_img: Image) -> Image:
        ...
        return raw_img

    def use_webcam(self, device: Webcam=None) -> Image:
        if device is None:
            if self.device is None:
                raise Exception("Need to specify a webcam device.")
            else:
                device = self.device
        raw_img = device.get_image()
        baked_img = self.process_webcam_input(raw_img)
        return baked_img
    
    def caption_image(self, image: Image) -> str:
        # invoke Moondream here.
        return caption