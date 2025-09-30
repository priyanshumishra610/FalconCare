import React, { useEffect, useState } from 'react';

const Hospitals = () => {
  const [loc, setLoc] = useState(null);
  const [hospitals, setHospitals] = useState([]);

  useEffect(() => {
    navigator.geolocation?.getCurrentPosition((pos) => {
      setLoc({ lat: pos.coords.latitude, lng: pos.coords.longitude });
    }, () => setLoc(null));
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const url = loc ? `http://localhost:5001/api/hospitals?lat=${loc.lat}&lng=${loc.lng}` : `http://localhost:5001/api/hospitals`;
        const res = await fetch(url);
        const data = await res.json();
        setHospitals(data.hospitals || []);
      } catch (_) {}
    })();
  }, [loc]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl font-bold mb-6">Nearby Hospitals</h1>
        <div className="space-y-4">
          {hospitals.map((h, idx) => (
            <div key={idx} className="bg-white rounded-xl shadow p-4">
              <div className="font-semibold">{h.name}</div>
              <div className="text-gray-600 text-sm">{h.address}</div>
              {h.location && (
                <a
                  href={`https://www.google.com/maps/dir/?api=1&destination=${h.location.lat},${h.location.lng}`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block mt-2 text-blue-600 hover:underline"
                >
                  Get Directions
                </a>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hospitals;


