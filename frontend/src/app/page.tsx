// src/app/page.tsx
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('mp4');
  const [message, setMessage] = useState('');

  const handleDownload = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/download/', {
        url,
        format,
      });
      setMessage(response.data.message);
    } catch (error) {
      // Controleer of de fout een AxiosError is
      if (axios.isAxiosError(error) && error.response) {
        setMessage('Error: ' + error.response.data.error);
      } else {
        setMessage('An unexpected error occurred');
      }
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>YouTube to MP3/MP4 Converter</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter YouTube URL"
        style={{ width: '300px', marginRight: '10px' }}
      />
      <select value={format} onChange={(e) => setFormat(e.target.value)}>
        <option value="mp4">MP4</option>
        <option value="mp3">MP3</option>
      </select>
      <button onClick={handleDownload}>Download</button>
      {message && <p>{message}</p>}
    </div>
  );
}
