import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const Blog = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch('http://localhost:5001/api/blog');
        const data = await res.json();
        setPosts(data);
      } catch (_) {}
      setLoading(false);
    })();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-5xl">
        <h1 className="text-4xl font-bold mb-6">Health Articles</h1>
        <p className="mb-6 text-gray-700">This is not medical advice. Please consult a doctor.</p>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {posts.map((p) => (
              <div key={p.id} className="bg-white rounded-xl shadow p-6">
                <h3 className="text-xl font-semibold">{p.title}</h3>
                <p className="text-gray-600 mt-2">{p.summary}</p>
                <div className="mt-4 flex justify-between items-center">
                  <span className="text-sm text-gray-500">{new Date(p.created_at).toLocaleDateString()}</span>
                  <Link to={`/blog/${p.id}`} className="text-blue-600 hover:underline">Read more</Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Blog;


