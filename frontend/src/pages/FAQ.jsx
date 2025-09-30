import React, { useEffect, useState } from 'react';

const FAQ = () => {
  const [items, setItems] = useState([]);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('http://localhost:5001/api/faq');
        const data = await res.json();
        setItems(data);
      } catch (_) {}
    })();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-6">FAQ</h1>
        <p className="mb-6 text-gray-700">This is not medical advice. Please consult a doctor.</p>
        <div className="space-y-4">
          {items.map((i) => (
            <details key={i.id} className="bg-white rounded-xl shadow p-4">
              <summary className="cursor-pointer font-semibold">{i.question}</summary>
              <p className="text-gray-700 mt-2 whitespace-pre-line">{i.answer}</p>
            </details>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FAQ;


