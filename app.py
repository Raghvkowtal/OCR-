from flask import Flask, request, render_template, redirect, url_for
import easyocr
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        recognized_text = ocr_scan(file_path)
        return render_template('result.html', text=recognized_text)

def ocr_scan(image_path):
    result = reader.readtext(image_path)
    recognized_text = " ".join(elem[1] for elem in result)
    return recognized_text

if __name__ == '__main__':
    app.run(debug=True)
