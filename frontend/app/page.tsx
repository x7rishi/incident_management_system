"use client";
import React, { useState } from 'react';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', email); // FastAPI OAuth2 expects 'username'
      formData.append('password', password);

      const res = await api.post('/auth/login', formData);
      localStorage.setItem('token', res.data.access_token);
      router.push('/dashboard');
    } catch (err) {
      alert("Invalid credentials. Try again.");
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <form onSubmit={handleLogin} className="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
        <h1 className="text-3xl font-extrabold text-slate-900 mb-6">Incident Engine</h1>
        <div className="space-y-4">
          <input 
            type="email" placeholder="Email" required
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-800"
            onChange={(e) => setEmail(e.target.value)}
          />
          <input 
            type="password" placeholder="Password" required
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-800"
            onChange={(e) => setPassword(e.target.value)}
          />
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-all shadow-md">
            Sign In
          </button>
        </div>
      </form>
    </main>
  );
}