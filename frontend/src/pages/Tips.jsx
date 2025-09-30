import React, { useEffect, useState } from 'react';

const Tips = () => {
  const [tip, setTip] = useState(null);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('http://localhost:5001/api/tips/daily');
        const data = await res.json();
        setTip(data.tip);
      } catch (_) {}
    })();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8">
        <h1 className="text-3xl font-bold">Daily Health Tip</h1>
        <p className="text-gray-700 mt-4">{tip || 'Loading...'}</p>
        <p className="text-xs text-gray-500 mt-6">This is not medical advice. Please consult a doctor.</p>
      </div>
    </div>
  );
};

export default Tips;


