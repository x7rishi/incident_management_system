"use client";
import React, { useEffect, useState } from 'react';
import api from '@/lib/api';

// 1. Types - Keeps our data structures strict
interface Incident {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
}

export default function Dashboard() {
  // --- States ---
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [search, setSearch] = useState('');
  
  // Modals & Drawers
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);

  // Form States
  const [newIncident, setNewIncident] = useState({ title: '', description: '', priority: 'medium' });
  const [editData, setEditData] = useState({ title: '', description: '' });

  // --- API Actions ---

  const fetchIncidents = async (query = '') => {
    try {
      // Switches to search endpoint if query length > 2
      const endpoint = query.length > 2 ? `/incidents/search?q=${query}` : '/incidents/';
      const res = await api.get(endpoint);
      setIncidents(res.data);
    } catch (err) {
      console.error("Fetch failed", err);
    }
  };

  useEffect(() => { fetchIncidents(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post('/incidents/', newIncident);
      setIncidents([res.data, ...incidents]); // Prepend new incident to list
      setIsModalOpen(false);
      setNewIncident({ title: '', description: '', priority: 'medium' });
    } catch (err) { alert("Check backend Pydantic validation (422 error)"); }
  };

  const handleResolve = async () => {
    if (!selectedIncident) return;
    try {
      await api.patch(`/incidents/${selectedIncident.id}`, { status: 'RESOLVED' });
      setIncidents(prev => prev.map(inc => 
        inc.id === selectedIncident.id ? { ...inc, status: 'RESOLVED' } : inc
      ));
      setSelectedIncident(null);
    } catch (err) { alert("Failed to resolve"); }
  };

  const startEditing = () => {
    if (!selectedIncident) return;
    setEditData({ title: selectedIncident.title, description: selectedIncident.description });
    setIsEditMode(true);
  };

  const handleUpdate = async () => {
    if (!selectedIncident) return;
    try {
      const res = await api.patch(`/incidents/${selectedIncident.id}`, editData);
      setIncidents(prev => prev.map(inc => inc.id === res.data.id ? res.data : inc));
      setSelectedIncident(res.data);
      setIsEditMode(false);
    } catch (err) { alert("Update failed"); }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 text-slate-900">
      <div className="max-w-6xl mx-auto">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10">
          <div>
            <h1 className="text-4xl font-black tracking-tight">Incident Engine</h1>
            <p className="text-slate-500 mt-1 font-medium">Core Management Dashboard</p>
          </div>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-emerald-100 transition-all active:scale-95"
          >
            + Report Incident
          </button>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <input 
            type="text"
            placeholder="Search incidents (Elasticsearch powered)..."
            className="w-full p-4 rounded-2xl border border-slate-200 shadow-sm outline-none focus:ring-4 focus:ring-blue-100 transition-all"
            onChange={(e) => {
              setSearch(e.target.value);
              fetchIncidents(e.target.value);
            }}
          />
        </div>

        {/* Main Incident Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {incidents.map((inc) => (
            <div 
              key={inc.id} 
              className={`group p-6 bg-white rounded-2xl border transition-all ${
                inc.status === 'RESOLVED' ? 'opacity-60 grayscale-[0.5] border-slate-100' : 'border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1'
              }`}
            >
              <div className="flex justify-between items-start mb-4">
                <span className={`text-[10px] font-black px-2 py-1 rounded-md uppercase ${
                  inc.priority === 'high' ? 'bg-rose-100 text-rose-600' : 'bg-sky-100 text-sky-600'
                }`}>
                  {inc.priority}
                </span>
                <span className="text-[10px] font-bold text-slate-400">ID: {inc.id.slice(0,8)}</span>
              </div>
              <h2 className="text-xl font-bold text-slate-800 line-clamp-1">{inc.title}</h2>
              <p className="text-slate-500 mt-2 text-sm leading-relaxed line-clamp-2">{inc.description}</p>
              
              <div className="mt-6 pt-4 border-t border-slate-50 flex justify-between items-center">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{inc.status}</span>
                <button 
                  onClick={() => { setSelectedIncident(inc); setIsEditMode(false); }}
                  className="text-blue-600 text-xs font-bold hover:underline"
                >
                  View Details →
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* --- MODAL: New Incident --- */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <form onSubmit={handleCreate} className="bg-white rounded-3xl p-8 max-w-lg w-full shadow-2xl animate-in fade-in zoom-in duration-200">
            <h2 className="text-2xl font-black mb-6">Report New Incident</h2>
            <div className="space-y-4">
              <input 
                placeholder="Title" required className="w-full p-4 bg-slate-50 border-none rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                value={newIncident.title} onChange={(e) => setNewIncident({...newIncident, title: e.target.value})}
              />
              <textarea 
                placeholder="Description" required className="w-full p-4 bg-slate-50 border-none rounded-xl h-32 outline-none focus:ring-2 focus:ring-blue-500"
                value={newIncident.description} onChange={(e) => setNewIncident({...newIncident, description: e.target.value})}
              />
              <select 
                className="w-full p-4 bg-slate-50 border-none rounded-xl outline-none focus:ring-2 focus:ring-blue-500"
                value={newIncident.priority} onChange={(e) => setNewIncident({...newIncident, priority: e.target.value})}
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
                <option value="critical">Critical</option>
              </select>
              <div className="flex gap-4 pt-4">
                <button type="button" onClick={() => setIsModalOpen(false)} className="flex-1 p-4 font-bold text-slate-400">Cancel</button>
                <button type="submit" className="flex-1 p-4 bg-blue-600 text-white rounded-xl font-bold">Create</button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* --- DRAWER: Details & Edit --- */}
      {selectedIncident && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          <div className="absolute inset-0 bg-slate-900/20 backdrop-blur-sm" onClick={() => setSelectedIncident(null)} />
          <div className="fixed inset-y-0 right-0 flex max-w-full pl-10">
            <div className="w-screen max-w-md bg-white shadow-2xl animate-in slide-in-from-right duration-300">
              <div className="flex h-full flex-col p-8">
                <div className="flex justify-between items-center mb-8">
                  <h2 className="text-2xl font-black">Incident Details</h2>
                  <button onClick={() => setSelectedIncident(null)} className="text-slate-400 hover:text-slate-900 text-2xl">✕</button>
                </div>

                <div className="space-y-6 overflow-y-auto flex-1">
                  <div>
                    <label className="text-[10px] font-black uppercase text-slate-400">Title</label>
                    {isEditMode ? (
                      <input className="w-full mt-1 p-3 border rounded-xl" value={editData.title} onChange={(e) => setEditData({...editData, title: e.target.value})} />
                    ) : (
                      <p className="text-xl font-bold text-slate-800 mt-1">{selectedIncident.title}</p>
                    )}
                  </div>

                  <div>
                    <label className="text-[10px] font-black uppercase text-slate-400">Description</label>
                    {isEditMode ? (
                      <textarea className="w-full mt-1 p-3 border rounded-xl h-40" value={editData.description} onChange={(e) => setEditData({...editData, description: e.target.value})} />
                    ) : (
                      <p className="text-slate-600 mt-2 p-4 bg-slate-50 rounded-xl leading-relaxed">{selectedIncident.description}</p>
                    )}
                  </div>
                </div>

                <div className="mt-auto pt-6 border-t flex gap-3">
                  {isEditMode ? (
                    <>
                      <button onClick={() => setIsEditMode(false)} className="flex-1 py-3 border rounded-xl font-bold">Cancel</button>
                      <button onClick={handleUpdate} className="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold">Save</button>
                    </>
                  ) : (
                    <>
                      {selectedIncident.status !== 'RESOLVED' && (
                        <button onClick={handleResolve} className="flex-1 py-3 bg-slate-900 text-white rounded-xl font-bold">Resolve</button>
                      )}
                      <button onClick={startEditing} className="flex-1 py-3 border rounded-xl font-bold">Edit</button>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}