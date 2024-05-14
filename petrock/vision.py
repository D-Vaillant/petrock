from PIL import Image
import cv2
from petrock.llms import summon_moondream
from openai import OpenAI
import io
import base64
import logging


class Webcam:
    def get_image(self, save_path=None) -> Image:
        raise NotImplementedError("Webcam class must implement `get_image()` method.")

class OpenCVWebcam(Webcam):
    def get_image(self, save_path=None) -> Image:
        cap = cv2.VideoCapture(0)  # Use the first webcam
        success, frame = cap.read()
        cap.release()
        if not success:
            raise Exception("Failed to capture image")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        if save_path:
            image.save(save_path)
        print("Using standard webcam via OpenCV.")
        return image


# Function to encode the image directly from a PIL Image object
def encode_image_to_base64(img: Image,

                           file_ext: str='JPEG') -> str:

    buffered = io.BytesIO()
    if file_ext.upper() == 'JPG':
        file_ext = 'JPEG'
    img.save(buffered, format=file_ext.upper())
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to encode the image
def encode_local_image(image_path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class Vision:
    def __init__(self, webcam: Webcam=None):
        self.webcam = webcam

    def caption_image(self, img: Image) -> str:
        base64_image = encode_image_to_base64(img)
        caption = self.send_image_to_moondream(base64_image)
        return caption

    def get_caption_from_image_path(self, image_path):
        # Capture image from webcam
        #image = self.webcam.get_image()
        # Encode image to base64
        base64_image = encode_local_image(image_path)
        caption = self.send_image_to_moondream(base64_image)
        return caption

    def send_image_to_moondream(self, base64_image):
        moondream = summon_moondream()
        response = moondream.chat.completions.create(
            model="moondream2",
            messages=[
                {"role": "system", "content": "You are an assistant who perfectly describes images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is in this image?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=300
        )
        try:
            return response.choices[0].message.content
        except IndexError as e:
            logging.error("Index error when getting response", exc_info=True)
            return "Error in processing image."
        except KeyError as k:
            logging.error("Key error when getting response", exc_info=True)
            return "Error in processing image."

def test_webcam_captioning():
    vision = Vision(webcam=OpenCVWebcam())
    image = vision.webcam.get_image()
    caption = vision.caption_image(image)
    print("Image Caption:", caption)

if __name__ == "__main__":
    test_webcam_captioning()
