import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const BlogPost = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`http://localhost:5001/api/blog/${id}`);
        const data = await res.json();
        setPost(data);
      } catch (_) {}
      setLoading(false);
    })();
  }, [id]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8">
        <Link to="/blog" className="text-blue-600 hover:underline">← Back to Articles</Link>
        {loading ? (
          <div className="mt-6">Loading...</div>
        ) : post ? (
          <div className="mt-6">
            <h1 className="text-3xl font-bold">{post.title}</h1>
            <p className="text-gray-500 mt-2">{new Date(post.created_at).toLocaleString()}</p>
            <p className="text-sm text-gray-600 mt-2">{post.disclaimer}</p>
            <div className="prose max-w-none mt-6 whitespace-pre-line">{post.content}</div>
          </div>
        ) : (
          <div className="mt-6">Not found</div>
        )}
      </div>
    </div>
  );
};

export default BlogPost;


