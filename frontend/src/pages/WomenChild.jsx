import React from 'react';

const WomenChild = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-4xl bg-white rounded-xl shadow p-8 space-y-6">
        <h1 className="text-3xl font-bold">Women & Child Health</h1>
        <p className="text-sm text-gray-500">This is not medical advice. Please consult a doctor.</p>
        <section>
          <h2 className="text-xl font-semibold">Pregnancy Tips</h2>
          <ul className="list-disc pl-6 text-gray-700 mt-2">
            <li>Take prenatal vitamins (as prescribed)</li>
            <li>Regular checkups and ultrasound scans</li>
            <li>Balanced diet, hydration, and light exercise</li>
          </ul>
        </section>
        <section>
          <h2 className="text-xl font-semibold">Breastfeeding Guidance</h2>
          <ul className="list-disc pl-6 text-gray-700 mt-2">
            <li>Initiate breastfeeding within first hour after birth</li>
            <li>Exclusive breastfeeding for first 6 months</li>
            <li>Seek lactation support if experiencing challenges</li>
          </ul>
        </section>
        <section>
          <h2 className="text-xl font-semibold">Child Nutrition Basics</h2>
          <ul className="list-disc pl-6 text-gray-700 mt-2">
            <li>Introduce complementary foods at 6 months</li>
            <li>Offer diverse foods rich in protein, iron, vitamins</li>
            <li>Maintain vaccination schedule</li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default WomenChild;


