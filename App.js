import React from 'react';
import OCR from './components/OCR';

function App() {
  return (
    <div className="App">
      <header style={{ textAlign: 'center' }}>
        <h1>Image to Text OCR</h1>
      </header>
      <OCR />
    </div>
  );
}

export default App;