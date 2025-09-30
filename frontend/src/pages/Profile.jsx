import React, { useEffect, useState } from 'react';

const API = 'http://localhost:5001';

const Profile = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [profile, setProfile] = useState({ age: '', gender: '', weight_kg: '', conditions: '' });

  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

  const fetchProfile = async () => {
    if (!token) return;
    const res = await fetch(`${API}/api/profile`, { headers: { ...authHeaders } });
    const data = await res.json();
    if (data && Object.keys(data).length > 0) setProfile(data);
  };

  useEffect(() => { fetchProfile(); }, [token]);

  const signup = async () => {
    const res = await fetch(`${API}/api/auth/signup`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
    const data = await res.json();
    if (data.accessToken) {
      localStorage.setItem('token', data.accessToken);
      setToken(data.accessToken);
    }
  };

  const login = async () => {
    const res = await fetch(`${API}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
    const data = await res.json();
    if (data.accessToken) {
      localStorage.setItem('token', data.accessToken);
      setToken(data.accessToken);
      fetchProfile();
    }
  };

  const save = async () => {
    await fetch(`${API}/api/profile`, { method: 'POST', headers: { 'Content-Type': 'application/json', ...authHeaders }, body: JSON.stringify(profile) });
    alert('Saved');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="container mx-auto max-w-3xl bg-white rounded-xl shadow p-8 space-y-6">
        <h1 className="text-3xl font-bold">User Health Profile</h1>
        <p className="text-sm text-gray-500">This is not medical advice. Please consult a doctor.</p>

        {!token && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2 items-end">
            <input className="border rounded p-2" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
            <input className="border rounded p-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            <div className="flex gap-2">
              <button onClick={signup} className="px-3 py-2 rounded bg-blue-600 text-white">Sign up</button>
              <button onClick={login} className="px-3 py-2 rounded bg-gray-800 text-white">Login</button>
            </div>
          </div>
        )}

        {token && (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input className="border rounded p-2" placeholder="Age" value={profile.age} onChange={e => setProfile({ ...profile, age: e.target.value })} />
              <input className="border rounded p-2" placeholder="Gender" value={profile.gender} onChange={e => setProfile({ ...profile, gender: e.target.value })} />
              <input className="border rounded p-2" placeholder="Weight (kg)" value={profile.weight_kg} onChange={e => setProfile({ ...profile, weight_kg: e.target.value })} />
              <input className="border rounded p-2" placeholder="Conditions (comma separated)" value={profile.conditions} onChange={e => setProfile({ ...profile, conditions: e.target.value })} />
            </div>
            <button onClick={save} className="px-4 py-2 rounded bg-blue-600 text-white">Save</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;


