from flask import Flask, render_template, request, jsonify
from vision import Vision  
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(BytesIO(image_data))
    
    vision = Vision()
    caption = vision.get_caption()

    return jsonify({'caption': caption})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
