import io
import base64
import logging
from pathlib import Path

from flask import (Flask, render_template, redirect, url_for,
                   request, g, jsonify, session)
from PIL import Image
import guidance
from guidance import user, assistant, system, gen
from petrock.llms import summon_llm
from petrock.vision import Vision
from petrock.entities import Petrock


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = "awdjaoiwjdioj3901u9"


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff'}

def allowed_file(filename: str) -> bool:
    suffix = Path(filename).suffix.lstrip('.')
    return suffix.lower() in ALLOWED_EXTENSIONS

# TODO: Allow user input to change rock personality.
personas = {
    'cool': ('chill', 'wax philosophical about nonsense'),
    'normal': ('boring', 'respond plainly and normally'),
    'angry': ('irritable', 'be rude for no reason')
}

petrock = Petrock(persona=('normal', 'act normally'),
                  capacities=[Vision()])

llm = summon_llm(model_name='llama3', echo=False)


def prompt_petrock(text_input: str, img_caption: str,
                   **kwargs) -> str:
    # TODO: Construct the prompt to the VLM.
    model = kwargs.get('model', 'llama3')
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


@app.route('/handle_caption', methods=['POST'])
def handle_caption():
    image_data = request.json['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    img_caption = petrock.vision.caption_image(image)

    session['petrock_response'] = img_caption

    logging.info(f"caption: {img_caption}")
    return jsonify({'caption': img_caption })


@app.route('/handle_response', methods=['POST'])
def handle_response():
    data = request.json  

    caption = data.get('caption')
    personality = data.get('personality', 'normal')
    logging.info(f"Selected personality: {personality}")

    prompt = "React to this caption as if you had seen an image."
    petrock.set_persona(*personas[personality])
    response = prompt_petrock(prompt, caption)
    return jsonify({'responseText' : response})
 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')




