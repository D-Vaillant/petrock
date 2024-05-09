from flask import Flask, render_template, redirect, url_for, request
from PIL import Image

app = Flask(__name__)

text_output = "Enter Text"
image_output = "Enter Image"
#Home Page 
@app.route('/')
def index():
    return render_template('index.html', text_output= text_output, image_output=image_output)


#Python functions
def average_pixel_brightness(img):
    
    # Convert image to grayscale
    img_gray = img.convert('L')
    
    # Get pixel data
    pixels = img_gray.getdata()
    
    # Calculate average brightness
    total_brightness = sum(pixels)
    num_pixels = len(pixels)
    average_brightness = total_brightness / num_pixels
    
    return average_brightness


@app.route('/handle_input', methods=['POST'])
def handle_input():
    global text_output
    global image_output

    #this handles the text input
    if 'text' in request.form:
         text = request.form['text']
         text_output = f'Text length is {len(text)}'

    else:
         text_output = "No text input"

    #This handles image input
    if 'file' in request.files:
         file = request.files['file']
         img = Image.open(file)
         #example function
         brightness = average_pixel_brightness(img)
         image_output = f"The average pixel brightness is {brightness}"

    else:
         image_output = 'No file part'
    
    
    return redirect(url_for('index'))



if __name__ == '__main__':
	app.run(debug = True)
     


