from flask import Flask, render_template, redirect, url_for, request, g
from PIL import Image
from vision import caption_image

app = Flask(__name__)

text_output = "Prompt"
image_output = "Image Upload / Webcam Upload"

def caption_image(img: Image) -> str:
    ...

def prompt_petrock(text_input: str, img_caption: str) -> str:
    
#Home Page 
@app.route('/')
def index():
    return render_template('index.html', text_output= text_output, image_output=image_output)


@app.route('/handle_input', methods=['POST'])
def handle_input():
    text_input = request.form.get('text', '')

    if 'file' in request.files:
        file = request.files['file']
        img = Image.open(file)
        #example function
        img_caption = caption_image(img)
    

    g.rock_response = prompt_petrock(text_input, img_caption)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug = True)



