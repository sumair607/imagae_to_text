import React, { useState } from 'react';
import { extractTextFromImage } from '../utils/ocr';

const OCR = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setText("");
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const result = await extractTextFromImage(file);
      setText(result);
    } catch (err) {
      setText("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <button onClick={handleUpload} disabled={!file || loading}>
        {loading ? "Processing..." : "Extract Text"}
      </button>

      {text && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <h3>Extracted Content:</h3>
          <p>{text}</p>
          <button onClick={() => navigator.clipboard.writeText(text)}>
            Copy to Clipboard
          </button>
        </div>
      )}
    </div>
  );
};

export default OCR;