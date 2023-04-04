from flask import Flask, request, jsonify, make_response, render_template, send_file
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # Get the image parameters from the form
    width = int(request.form['width'])
    height = int(request.form['height'])
    color = request.form['color']
    img_format = request.form['format']

    # Validate the image parameters
    if width <= 0 or height <= 0 or color not in ['red', 'green', 'blue'] or img_format not in ['jpeg', 'png', 'gif']:
        return make_response(jsonify({'error': 'Invalid image parameters.'}), 400)

    # Generate the image
    if color == 'red':
        img = Image.new('RGB', (width, height), (255, 0, 0))
    elif color == 'green':
        img = Image.new('RGB', (width, height), (0, 255, 0))
    else:
        img = Image.new('RGB', (width, height), (0, 0, 255))

    # Save the image to a file
    filename = 'generated_image.' + img_format
    img.save(filename)

    # Return the filename as a response
    return make_response(jsonify({'filename': filename}), 200)

@app.route('/get-image/<filename>')
def get_image(filename):
    return send_file(filename, mimetype='image/' + filename.split('.')[-1])

if __name__ == '__main__':
    app.run(debug=True)
