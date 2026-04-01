from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

OCR_API_KEY = os.environ.get('OCR_SPACE_API_KEY', '')

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

        img_bytes = file.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        ext = file.filename.rsplit('.', 1)[-1].lower()
        mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'

        payload_base = {
            'base64Image': f'data:{mime};base64,{img_base64}',
            'apikey': OCR_API_KEY,
            'language': 'auto',
            'isOverlayRequired': False,
            'scale': True,
            'detectOrientation': True,
        }

        engines = [2, 1]

        extracted_text = ''
        for engine in engines:
            try:
                response = requests.post(
                    'https://api.ocr.space/parse/image',
                    data={**payload_base, 'OCREngine': engine},
                    timeout=60
                )
                result = response.json()
                if not isinstance(result, dict):
                    continue
                if result.get('IsErroredOnProcessing'):
                    continue
                parsed = result.get('ParsedResults', [])
                extracted_text = parsed[0].get('ParsedText', '').strip() if parsed else ''
                if extracted_text:
                    break
            except (requests.exceptions.Timeout, ValueError):
                continue

        if not extracted_text:
            extracted_text = 'No text found in image'

        return jsonify({'success': True, 'text': extracted_text})

    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
