from PIL import Image
import cv2
from petrock.llms import summon_moondream
from openai import OpenAI
import io
import base64
import requests

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
    img.save(buffered, format="JPG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to encode the image
def encode_local_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def summon_moondream():
    # Returns an initialized OpenAI object configured to communicate with your server
    return OpenAI(api_key='moondream', base_url='http://localhost:8080/v1')

class Vision:
    #def __init__(self, webcam):
   #     self.webcam = webcam

    def get_caption(self, image_path):
        # Capture image from webcam
        #image = self.webcam.get_image()
        # Encode image to base64
        base64_image = encode_local_image(image_path)
        
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
        if 'choices' in response and response['choices']:
            return response['choices'][0]['message']['content']
        else:
            return "No caption generated."
    
def test_vision_system():
    # webcam = OpenCVWebcam()
    vision = Vision()
    image_path = '../images/cat.jpg'
    #image = vision.use_webcam()
    caption = vision.get_caption(image_path)
    print("Image Caption:", caption)

if __name__ == "__main__":
    test_vision_system()