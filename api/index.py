# Image to Text Flask App
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pytesseract
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
            extracted_text = pytesseract.image_to_string(image)
            
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