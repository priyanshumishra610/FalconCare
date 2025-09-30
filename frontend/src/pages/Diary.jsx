import React, { useEffect, useState } from 'react';

const API = 'http://localhost:5001';

const Diary = () => {
  const [entries, setEntries] = useState([]);
  const [date, setDate] = useState('');
  const [notes, setNotes] = useState('');
  const [symptoms, setSymptoms] = useState('');

  const token = localStorage.getItem('token');
  const headers = token ? { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };

  const fetchEntries = async () => {
    if (!token) return;
    const res = await fetch(`${API}/api/diary`, { headers });
    const data = await res.json();
    setEntries(data);
  };

  useEffect(() => { fetchEntries(); }, []);

  const add = async () => {
    await fetch(`${API}/api/diary`, { method: 'POST', headers, body: JSON.stringify({ date, notes, symptoms: symptoms.split(',').map(s => s.trim()) }) });
    setDate(''); setNotes(''); setSymptoms('');
    fetchEntries();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8">
        <h1 className="text-3xl font-bold">Health Diary</h1>
        <p className="text-sm text-gray-500">This is not medical advice. Please consult a doctor.</p>
        {!token && <p className="mt-4 text-red-600">Login on Profile page to use diary.</p>}
        {token && (
          <div className="mt-6 space-y-3">
            <input className="border rounded p-2 w-full" type="date" value={date} onChange={e => setDate(e.target.value)} />
            <input className="border rounded p-2 w-full" placeholder="Symptoms (comma separated)" value={symptoms} onChange={e => setSymptoms(e.target.value)} />
            <textarea className="border rounded p-2 w-full" rows="4" placeholder="Notes" value={notes} onChange={e => setNotes(e.target.value)} />
            <button onClick={add} className="px-4 py-2 rounded bg-blue-600 text-white">Add Entry</button>
          </div>
        )}
        <div className="mt-8 space-y-3">
          {entries.map(e => (
            <div key={e.id} className="border rounded p-4">
              <div className="text-sm text-gray-500">{new Date(e.date).toLocaleDateString()}</div>
              <div className="font-semibold">Symptoms: {e.symptoms}</div>
              <div className="text-gray-700 whitespace-pre-line">{e.notes}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Diary;


