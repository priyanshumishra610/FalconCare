import React, { useEffect, useState } from 'react';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('http://localhost:5001/api/alerts');
        const data = await res.json();
        setAlerts(data.alerts || []);
      } catch (_) {}
    })();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-6">Outbreak Alerts</h1>
        <div className="space-y-4">
          {alerts.map((a, idx) => (
            <div key={idx} className="bg-white rounded-xl shadow p-4 border-l-4 border-red-500">
              <div className="text-sm text-gray-500">{a.region}</div>
              <div className="font-semibold mt-1">{a.message}</div>
              <div className="text-xs mt-1 uppercase tracking-wide text-red-600">{a.severity}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Alerts;


