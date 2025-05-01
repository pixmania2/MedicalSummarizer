import React, { useState, useEffect } from 'react';

async function getJSON(url, opts) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export default function PdfUploader() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState('');
  const [meta, setMeta] = useState(null);
  const [pdfURL, setPdfURL] = useState('');

  const handleUpload = async () => {
    const form = new FormData();
    form.append('file', file);
    const { job_id } = await getJSON('/api/summarize', { method: 'POST', body: form });
    setJobId(job_id);
    setStatus('queued');
  };

  useEffect(() => {
    if (!jobId) return;
    const iv = setInterval(async () => {
      try {
        const { status } = await getJSON(`/api/status/${jobId}`);
        setStatus(status);
        if (status === 'success') {
          clearInterval(iv);
          const data = await getJSON(`/api/result/${jobId}`);
          setMeta(data);
          const pdfRes = await fetch(`/api/download/${jobId}`);
          const blob = await pdfRes.blob();
          setPdfURL(URL.createObjectURL(blob));
        }
      } catch {}
    }, 3000);
    return () => clearInterval(iv);
  }, [jobId]);

  return (
    <div className="space-y-4">
      <input type="file" accept="application/pdf" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={!file || jobId} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
        Upload & Summarize
      </button>
      {status && <p>Status: {status}</p>}
      {meta && (
        <>
          <h2 className="text-lg font-semibold">Abstractive Summary</h2>
          <p>{meta.summary}</p>
          <h2 className="text-lg font-semibold mt-4">Extracted Information</h2>
          <ul className="list-disc ml-6">
            {Object.entries(meta.entities).map(([slot, vals]) => (
              <li key={slot}><b>{slot}</b>: {vals.join(', ')}</li>
            ))}
          </ul>
        </>
      )}
      {pdfURL && (
        <>
          <h2 className="text-lg font-semibold mt-4">Summarized PDF</h2>
          <iframe title="summary-pdf" src={pdfURL} className="w-full h-96 border" />
          <a href={pdfURL} download={`summary_${jobId}.pdf`} className="block mt-2 text-blue-600">Download PDF</a>
        </>
      )}
    </div>
);
}