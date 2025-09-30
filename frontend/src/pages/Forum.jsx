import React, { useEffect, useState } from 'react';

const Forum = () => {
  const [posts, setPosts] = useState([]);
  const [content, setContent] = useState('');

  const fetchPosts = async () => {
    const res = await fetch('http://localhost:5001/api/forum');
    const data = await res.json();
    setPosts(data);
  };

  useEffect(() => { fetchPosts(); }, []);

  const create = async () => {
    await fetch('http://localhost:5001/api/forum', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content }) });
    setContent('');
    fetchPosts();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl">
        <h1 className="text-3xl font-bold mb-4">Anonymous Forum</h1>
        <p className="text-sm text-gray-500">This is not medical advice. Please consult a doctor.</p>
        <div className="bg-white rounded-xl shadow p-4 mt-4">
          <textarea className="w-full border rounded p-2" rows="3" placeholder="Share your question or experience anonymously..." value={content} onChange={e => setContent(e.target.value)} />
          <button onClick={create} className="mt-2 px-4 py-2 rounded bg-blue-600 text-white">Post</button>
        </div>
        <div className="mt-6 space-y-3">
          {posts.map(p => (
            <div key={p.id} className="bg-white rounded-xl shadow p-4">
              <div className="text-sm text-gray-500">{new Date(p.created_at).toLocaleString()}</div>
              <div className="mt-2 whitespace-pre-line">{p.content}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Forum;


