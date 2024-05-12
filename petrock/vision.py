from PIL import Image

import cv2
import io
import base64
import logging

from petrock.llms import summon_moondream


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


# Function to encode the image directly from a PIL Image object
def encode_image_to_base64(img: Image) -> str:
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
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
        # Prepare message for local model
        moondream = summon_moondream()
        response = moondream.chat.completions.create(
            model="moondream2",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "What’s in this image?"
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                        }
                    ]
                }
            ],
            max_tokens=300
            )
        # Extract the response
        try:
            return response.choices[0].message.content
        except IndexError as e:
            logging.fatal("Index error when getting response")
            raise e
        except KeyError as k:
            logging.fatal("Key error when getting response")
            raise k



def test_vision_system():
    # webcam = OpenCVWebcam()
    vision = Vision()
    image_path = 'images/cat.jpg'
    #image = vision.use_webcam()
    caption = vision.get_caption_from_image_path(image_path)
    print("Image Caption:", caption)

if __name__ == "__main__":
    test_vision_system()
