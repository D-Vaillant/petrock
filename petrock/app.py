from flask import Flask, render_template, request, jsonify
from vision import Vision  
import base64
from io import BytesIO
from PIL import Image

from petrock import Petrock

petrock = Petrock(persona=('chill', 'making people laugh'),
                  capacities=[Vision()])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route of functions involved.
# 1. Either an image upload or a webcam upload. Either way, we can access the image the same way.
# 
@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(BytesIO(image_data))
    caption = petrock.vision.caption_image(image)
    return jsonify({'caption': caption})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
