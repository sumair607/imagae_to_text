# Image to Text Flask App
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
import base64
from PIL import Image
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for WordPress integration

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """Extract text from uploaded image using OCR"""
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            file.save(temp_file.name)
            
            # Open image and extract text
            image = Image.open(temp_file.name)
            # Convert image to base64
            with open(temp_file.name, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Use Google Vision API (free tier: 1000 requests/month)
            api_key = os.environ.get('GOOGLE_VISION_API_KEY', 'demo')
            if api_key == 'demo':
                extracted_text = "Demo mode: Please add GOOGLE_VISION_API_KEY environment variable"
            else:
                url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'
                payload = {
                    'requests': [{
                        'image': {'content': img_base64},
                        'features': [{'type': 'TEXT_DETECTION'}]
                    }]
                }
                response = requests.post(url, json=payload)
                result = response.json()
                extracted_text = result['responses'][0].get('fullTextAnnotation', {}).get('text', 'No text found')
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return jsonify({
                'success': True,
                'text': extracted_text.strip()
            })
    
    except Exception as e:
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

# For Vercel deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# Export app for Vercel
app = app