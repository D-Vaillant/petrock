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

def encode_image_to_base64(img: Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def summon_moondream():
    # Returns an initialized OpenAI object configured to communicate with your server
    return OpenAI(api_key='moondream', base_url='http://localhost:8080/v1')

class Vision:
    def __init__(self):
        self.webcam = OpenCVWebcam()

    def get_caption(self, save_path="./tmp/captured_image.jpg"):
        image = self.webcam.get_image(save_path=save_path)
        base64_image = encode_image_to_base64(image)
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

def test_vision_system():
    vision = Vision()
    caption = vision.get_caption()
    print("Image Caption:", caption)

if __name__ == "__main__":
    test_vision_system()