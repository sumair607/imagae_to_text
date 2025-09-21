# Picture to Text OCR App

A simple web application that extracts text from images using OCR (Optical Character Recognition).

## Features
- Upload images (PNG, JPG, JPEG, etc.)
- Extract text using Tesseract OCR
- Copy extracted text to clipboard
- Clean, responsive web interface

## Installation

### Prerequisites
- Python 3.7+
- Tesseract OCR engine

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and go to: `http://localhost:5000`

3. Upload an image and click "Extract Text"

## Project Structure
```
picture-to-text/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend HTML
├── static/
│   └── style.css      # CSS styles
└── README.md          # This file
```

## Future Extensions

### Mobile App
- Use Capacitor/Cordova to wrap the web app
- Add camera capture functionality
- Implement offline OCR processing

### AWS Deployment
- Deploy to AWS Elastic Beanstalk or EC2
- Use AWS Textract for better OCR accuracy
- Store images in S3 bucket
- Add user authentication with Cognito

### Enhancements
- Support multiple languages
- Batch processing
- PDF text extraction
- Text translation
- Export to various formats

## Troubleshooting

**Tesseract not found error:**
- Ensure Tesseract is installed and in PATH
- On Windows, add Tesseract installation path to system PATH

**Large file upload errors:**
- Check Flask's MAX_CONTENT_LENGTH setting
- Compress images before upload# imagae_to_text
