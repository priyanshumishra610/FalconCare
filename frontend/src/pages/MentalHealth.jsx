import React from 'react';

const MentalHealth = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8 space-y-4">
        <h1 className="text-3xl font-bold">Mental Health Support</h1>
        <p className="text-gray-700">If you feel overwhelmed or in crisis, please reach out immediately.</p>
        <div className="bg-yellow-50 border border-yellow-200 rounded p-4">
          <div className="font-semibold">India Helplines</div>
          <ul className="list-disc pl-6 text-gray-700 mt-2">
            <li>KIRAN Helpline: 1800-599-0019</li>
            <li>Emergency: 112</li>
          </ul>
        </div>
        <p className="text-sm text-gray-500">This is not medical advice. Please consult a qualified professional.</p>
      </div>
    </div>
  );
};

export default MentalHealth;


