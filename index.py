from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image
import os
import tempfile

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            image = Image.open(temp_file.name)
            reader = easyocr.Reader(['en'])
            result = reader.readtext(image)
            extracted_text = ' '.join([item[1] for item in result])
            os.unlink(temp_file.name)
            
            return jsonify({
                'success': True,
                'text': extracted_text.strip()
            })
    
    except Exception as e:
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)