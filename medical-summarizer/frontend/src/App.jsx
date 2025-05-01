import React from 'react';
import PdfUploader from './components/PdfUploader';

export default function App() {
  return (
    <div className="min-h-screen p-6">
      <h1 className="text-2xl font-bold mb-4">Medical Report Summarizer</h1>
      <PdfUploader />
    </div>
  );
}
