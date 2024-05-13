import io
import base64
import logging

from flask import (Flask, render_template, redirect, url_for,
                   request, g, jsonify)
from PIL import Image
import guidance
from guidance import user, assistant, system, gen
from petrock.llms import summon_llm
from petrock.vision import Vision
from petrock.entities import Petrock
import base64
import io



logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'super_special_secret_key'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO: Allow user input to change rock personality.
petrock = Petrock(persona=('chill', 'making people laugh'),
                  capacities=[Vision()])



def prompt_petrock(text_input: str, img_caption: str,
                   **kwargs) -> str:
    # TODO: Construct the prompt to the VLM.
    model = kwargs.get('model', 'llama3')
    llm = summon_llm(model)
    # We start with returning the whole thing at once.
    # Then we can tackle streaming.
    # get some guidance program
    prompt = f"Caption: {img_caption}\n{text_input}."
    llm_a = llm + petrock.chat(prompt)
    return llm_a['response']



#Home Page 
@app.route('/')
def index():
    #petrock_response = session.get('petrock_response', None)
    g.vibe = petrock.persona.vibe
    g.purpose = petrock.persona.purpose
    
    return render_template('index.html', vibe = g.vibe, purpose = g.purpose)



@app.route('/handle_capture', methods=['POST'])
def handle_capture():
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    img_caption = petrock.vision.caption_image(image)
    session['petrock_response'] = img_caption
    return jsonify({'caption': img_caption})

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    caption = petrock.vision.caption_image(image)
    logging.info(f"caption: {caption}")
    return jsonify({'caption': caption})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    app.run(debug = True)



