from PIL import Image
import cv2
from llms import summon_moondream

#if webcam has error
class Webcam:
    def get_image(self) -> Image:
        raise NotImplementedError("Webcam class must implement `get_image()` method.")

#capture image from cam, using openCV and return as PIL Image.
class OpenCVWebcam(Webcam):
    def get_image(self) -> Image:
        cap = cv2.VideoCapture(0)  # 0 is usually the default camera
        success, frame = cap.read()
        cap.release()
        if not success:
            raise Exception("Failed to capture image")
        # Convert the color from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame)

class Vision:
    def __init__(self, device: Webcam = None):
        self.device = device or OpenCVWebcam()  # Default to OpenCVWebcam if no device is provided

    # Future processing can be added here, such as resizing or filtering. currently raw image
    def process_webcam_input(self, raw_img: Image) -> Image:
        return raw_img

    #capture image and process it
    def use_webcam(self, device: Webcam=None) -> Image:
        if device is None:
            if self.device is None:
                raise Exception("Need to specify a webcam device.")
            else:
                device = self.device
        raw_img = device.get_image()
        baked_img = self.process_webcam_input(raw_img)
        return baked_img
    
    #use moondream model to generate caption for the image.
    def caption_image(self) -> str:
        img = self.use_webcam()
        temp_image_path = "/tmp/captured_image.png" # Save temp image
        img.save(temp_image_path)
        moondream = summon_moondream() # Summon the Moondream model  
        caption = moondream.describe_image(temp_image_path)
        return caption

if __name__ == "__main__":
    vision = Vision()
    try:
        caption = vision.caption_image()
        print(f"Generated Caption: {caption}")
    except Exception as e:
        print(f"An error occurred: {e}")