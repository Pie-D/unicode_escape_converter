from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_to_unicode_escape(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    try:
        decoded_content = content.encode('utf-8').decode('unicode_escape')
    except UnicodeDecodeError:
        decoded_content = content
    escaped_content = decoded_content.encode('unicode_escape').decode('ascii')
    with open(output_path, 'w', encoding='ascii') as outfile:
        outfile.write(escaped_content)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return 'No file selected', 400
        input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, 'output.txt')
        uploaded_file.save(input_path)
        convert_to_unicode_escape(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
