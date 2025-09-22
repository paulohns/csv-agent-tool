import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([]);
  const [chartData, setChartData] = useState(null);

  // Upload CSV
  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8001/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (res.ok) {
        setFilename(data.filename);
        alert('Arquivo enviado com sucesso!');
      } else {
        alert('Erro ao enviar arquivo: ' + data.message);
      }
    } catch (err) {
      alert('Erro ao enviar arquivo: ' + err.message);
    }
  };

  // Perguntar à LLM
  const handleAsk = async () => {
    if (!question) return;
    try {
      const res = await fetch('http://localhost:8001/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ pergunta: question }),
      });
      const data = await res.json();
      const ans = data.response.output;
      setResponse(ans);
      setHistory(prev => [...prev, { q: question, a: ans }]);
      setQuestion('');

      // Detectar dados tabulares
      try {
        const parsed = JSON.parse(ans);
        if (Array.isArray(parsed)) setChartData(parsed);
        else setChartData(null);
      } catch { setChartData(null); }

    } catch (err) {
      alert('Erro ao fazer pergunta: ' + err.message);
    }
  };

  return (
    <div className="container my-4">
      <h1 className="text-center mb-4">EDA CSV com LangChain + Groq</h1>

      {/* Upload CSV */}
      <div className="card mb-4 p-3">
        <div className="d-flex align-items-center">
          <input type="file" accept=".csv" className="form-control" onChange={e => setFile(e.target.files[0])} />
          <button className="btn btn-primary ms-2" onClick={handleUpload}>Upload CSV</button>
        </div>
      </div>

      {/* Formulário de perguntas */}
      {filename && (
        <div className="card mb-4 p-3">
          <p><strong>Arquivo atual:</strong> {filename}</p>
          <textarea
            className="form-control mb-2"
            placeholder="Digite sua pergunta sobre os dados..."
            value={question}
            onChange={e => setQuestion(e.target.value)}
          />
          <button className="btn btn-success" onClick={handleAsk}>Perguntar</button>
        </div>
      )}

      {/* Resposta */}
      {response && (
        <div className="card mb-4 p-3">
          <h5>Resposta:</h5>
          <p>{response}</p>
        </div>
      )}

      {/* Gráfico */}
      {chartData && (
        <div className="card mb-4 p-3">
          <h5>Visualização</h5>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={Object.keys(chartData[0])[0]} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={Object.keys(chartData[0])[1]} stroke="#007bff" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Histórico */}
      {history.length > 0 && (
        <div className="card mb-4 p-3">
          <h5>Histórico de Perguntas/Respostas</h5>
          {history.map((h, idx) => (
            <div key={idx} className="mb-2 p-2 border rounded">
              <p className="mb-1"><strong>P:</strong> {h.q}</p>
              <p className="mb-0"><strong>R:</strong> {h.a}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
