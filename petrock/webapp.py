from flask import Flask, render_template, redirect, url_for, request, g
from PIL import Image
import guidance
from guidance import user, assistant, system, gen
from petrock.llms import summon_llm
from petrock.vision import Vision
from petrock.entities import Petrock


app = Flask(__name__)


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
    g.vibe = petrock.persona.vibe
    g.purpose = petrock.persona.purpose
    return render_template('index.html', g=g)


@app.route('/handle_input', methods=['POST'])
def handle_input():
    g.vibe = petrock.persona.vibe
    g.purpose = petrock.persona.purpose
    # text_input = request.form.get('text', '')

    if 'file' in request.files:
        file = request.files['file']
        img = Image.open(file)
        #example function
        img_caption = 'A majestic sunrise.'
        # img_caption = petrock.vision.caption_image(img)

    g.rock_response = prompt_petrock('React as if you had been presented with an image matching this caption.',
                                     img_caption)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug = True)



