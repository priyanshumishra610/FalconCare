import React, { useMemo, useState } from 'react';

const QUIZ = [
  { q: 'Dengue is transmitted by which mosquito?', a: ['Anopheles', 'Aedes aegypti', 'Culex'], c: 1 },
  { q: 'Which vitamin is primarily from sunlight exposure?', a: ['Vitamin C', 'Vitamin D', 'Vitamin B12'], c: 1 },
  { q: 'Handwashing should take at least?', a: ['5 seconds', '20 seconds', '1 minute'], c: 1 },
  { q: 'Polio vaccine is given to?', a: ['Adults only', 'Children', 'Elderly only'], c: 1 },
  { q: 'Best way to prevent malaria?', a: ['Antibiotics', 'Mosquito nets & repellents', 'Vitamin supplements'], c: 1 },
];

const Quiz = () => {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const score = useMemo(() => {
    if (!submitted) return 0;
    return QUIZ.reduce((s, item, i) => (answers[i] === item.c ? s + 1 : s), 0);
  }, [submitted, answers]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8">
        <h1 className="text-3xl font-bold">Health Quiz</h1>
        {!submitted ? (
          <div className="mt-6 space-y-6">
            {QUIZ.map((item, i) => (
              <div key={i}>
                <div className="font-semibold">{i + 1}. {item.q}</div>
                <div className="mt-2 grid grid-cols-1 gap-2">
                  {item.a.map((opt, idx) => (
                    <label key={idx} className="flex items-center gap-2">
                      <input type="radio" name={`q${i}`} checked={answers[i] === idx} onChange={() => setAnswers({ ...answers, [i]: idx })} />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
            <button onClick={() => setSubmitted(true)} className="px-4 py-2 rounded bg-blue-600 text-white">Submit</button>
          </div>
        ) : (
          <div className="mt-6">
            <div className="text-xl font-semibold">Your score: {score} / {QUIZ.length}</div>
            <div className="mt-2">{score === QUIZ.length ? '🏅 Perfect!' : score >= 3 ? '🎉 Great job!' : 'Keep learning!'}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Quiz;


