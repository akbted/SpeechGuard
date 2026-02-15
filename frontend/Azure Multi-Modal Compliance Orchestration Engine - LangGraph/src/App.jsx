import React, { useState } from 'react';
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  Video, 
  Activity, 
  FileText, 
  Search, 
  AlertCircle,
  Clock,
  ChevronDown,
  ChevronUp,
  X
} from 'lucide-react';

// --- Components ---

const SeverityBadge = ({ level }) => {
  const normalized = level?.toLowerCase() || 'low';
  
  const styles = {
    high: 'bg-red-100 text-red-800 border-red-200',
    medium: 'bg-orange-100 text-orange-800 border-orange-200',
    low: 'bg-green-100 text-green-800 border-green-200',
    critical: 'bg-red-800 text-white border-red-900'
  };

  const style = styles[normalized] || styles.low;

  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${style} uppercase tracking-wide`}>
      {level}
    </span>
  );
};

const IssueCard = ({ issue }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-3 hover:shadow-sm transition-shadow">
      <div className="flex justify-between items-start cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <div className="flex gap-3">
            <div className={`mt-1 p-1.5 rounded-full ${issue.severity.toLowerCase() === 'high' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'}`}>
                <AlertTriangle size={18} />
            </div>
            <div>
                <h4 className="font-semibold text-gray-900">{issue.category}</h4>
                <div className="flex items-center gap-2 text-sm text-gray-500 mt-1">
                    <Clock size={14} />
                    <span>Timestamp: {issue.time_stamp || 'N/A'}</span>
                </div>
            </div>
        </div>
        <div className="flex items-center gap-3">
             <SeverityBadge level={issue.severity} />
             {expanded ? <ChevronUp size={18} className="text-gray-400" /> : <ChevronDown size={18} className="text-gray-400" />}
        </div>
      </div>

      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-100 pl-11">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <p className="text-xs font-semibold text-gray-500 uppercase">Description</p>
                    <p className="text-sm text-gray-700 mt-1">{issue.description}</p>
                </div>
                <div>
                    <p className="text-xs font-semibold text-gray-500 uppercase">Flagged Text</p>
                    <p className="text-sm font-mono bg-gray-50 text-gray-800 p-2 rounded mt-1 border border-gray-200">
                        "{issue.flagged_text || 'No text segment identified'}"
                    </p>
                </div>
                {issue.legal_reference && (
                     <div className="md:col-span-2">
                        <p className="text-xs font-semibold text-gray-500 uppercase">Legal Reference</p>
                        <p className="text-sm text-gray-600 mt-1 italic">{issue.legal_reference}</p>
                    </div>
                )}
            </div>
        </div>
      )}
    </div>
  );
};

export default function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleAudit = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      // Assuming backend is running on localhost:8000
      const response = await fetch('http://localhost:8000/audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: url }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server Error: ${response.status}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error(err);
      setError(err.message === 'Failed to fetch' 
        ? 'Could not connect to backend. Is it running on port 8000 with CORS enabled?' 
        : err.message
      );
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'completed': return 'text-green-600 bg-green-50 border-green-200';
      case 'failed': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-blue-600 bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 p-2 rounded-lg">
                <Shield className="text-white" size={24} />
            </div>
            <div>
                <h1 className="text-xl font-bold text-gray-900 tracking-tight">Drishti</h1>
                <p className="text-xs text-gray-500 font-medium">AI Compliance & Hate Speech Analyzer</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 rounded-full bg-gray-100 text-xs font-medium text-gray-600">v1.0.0</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Input Section */}
        <div className="max-w-3xl mx-auto mb-12">
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Audit Video Content</h2>
                <p className="text-gray-500">Enter a video URL to generate a comprehensive compliance report and detect potential hate speech violations.</p>
            </div>

            <form onSubmit={handleAudit} className="relative">
                <div className="flex shadow-lg rounded-xl overflow-hidden border border-gray-200 bg-white">
                    <div className="pl-4 flex items-center justify-center bg-gray-50 border-r border-gray-200">
                         <Video className="text-gray-400" size={20} />
                    </div>
                    <input 
                        type="url" 
                        placeholder="https://example.com/video-source.mp4" 
                        className="flex-1 px-4 py-4 focus:outline-none focus:ring-0 text-gray-700 placeholder-gray-400"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        required
                    />
                    <button 
                        type="submit" 
                        disabled={loading}
                        className={`px-8 font-semibold text-white transition-all ${
                            loading 
                            ? 'bg-indigo-400 cursor-not-allowed' 
                            : 'bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800'
                        }`}
                    >
                        {loading ? (
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                Analyzing...
                            </div>
                        ) : (
                            <div className="flex items-center gap-2">
                                <Activity size={18} />
                                Run Audit
                            </div>
                        )}
                    </button>
                </div>
            </form>

            {/* Error Message */}
            {error && (
                <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3 animate-fade-in">
                    <AlertCircle className="text-red-600 mt-0.5" size={20} />
                    <div>
                        <h4 className="font-semibold text-red-900">Analysis Failed</h4>
                        <p className="text-red-700 text-sm mt-1">{error}</p>
                    </div>
                </div>
            )}
        </div>

        {/* Results Section */}
        {data && (
            <div className="space-y-8 animate-fade-in">
                
                {/* 1. High Level Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Session Info */}
                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-gray-500 text-sm font-medium uppercase tracking-wider">Session Status</h3>
                            <Activity size={20} className="text-gray-400" />
                        </div>
                        <div className="flex items-center gap-3">
                            <span className={`px-3 py-1 rounded-full text-sm font-bold border ${getStatusColor(data.status)}`}>
                                {data.status || 'UNKNOWN'}
                            </span>
                        </div>
                        <div className="mt-4 pt-4 border-t border-gray-100 text-xs text-gray-400 flex flex-col gap-1 font-mono">
                            <span>SID: {data.session_id}</span>
                            <span>VID: {data.video_id}</span>
                        </div>
                    </div>

                    {/* Issue Count */}
                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-gray-500 text-sm font-medium uppercase tracking-wider">Issues Detected</h3>
                            <AlertTriangle size={20} className="text-gray-400" />
                        </div>
                        <div className="flex items-end gap-2">
                            <span className="text-4xl font-bold text-gray-900">{data.compliance_results?.length || 0}</span>
                            <span className="text-gray-500 mb-1.5">alerts found</span>
                        </div>
                    </div>

                    {/* Risk Assessment (Mock logic based on count) */}
                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-gray-500 text-sm font-medium uppercase tracking-wider">Risk Level</h3>
                            <Shield size={20} className="text-gray-400" />
                        </div>
                        <div className="flex items-center gap-2">
                            {(data.compliance_results?.length || 0) > 0 ? (
                                <span className="text-red-600 font-bold text-xl">High Risk Content</span>
                            ) : (
                                <span className="text-green-600 font-bold text-xl">Safe Content</span>
                            )}
                        </div>
                        <p className="text-xs text-gray-400 mt-2">Based on automated AI audit.</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    
                    {/* 2. Detailed Findings List */}
                    <div className="lg:col-span-2 space-y-6">
                        <div className="flex items-center justify-between">
                            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                                <FileText size={20} className="text-indigo-600" />
                                Detailed Findings
                            </h3>
                        </div>

                        {data.compliance_results && data.compliance_results.length > 0 ? (
                            <div className="space-y-1">
                                {data.compliance_results.map((issue, index) => (
                                    <IssueCard key={index} issue={issue} />
                                ))}
                            </div>
                        ) : (
                            <div className="bg-white border border-gray-200 rounded-lg p-12 text-center">
                                <div className="mx-auto w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-4">
                                    <CheckCircle size={32} />
                                </div>
                                <h3 className="text-lg font-medium text-gray-900">No Compliance Issues Found</h3>
                                <p className="text-gray-500 mt-1">The video passed all hate speech and compliance checks.</p>
                            </div>
                        )}
                    </div>

                    {/* 3. Final Report Summary */}
                    <div className="lg:col-span-1">
                        <div className="bg-indigo-900 text-white rounded-xl shadow-lg p-6 sticky top-24">
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <Shield className="text-indigo-300" size={20} />
                                Executive Summary
                            </h3>
                            <div className="prose prose-invert prose-sm">
                                <p className="text-indigo-100 leading-relaxed whitespace-pre-wrap">
                                    {data.final_report || "No summary report available."}
                                </p>
                            </div>
                            
                            {data.errors && data.errors.length > 0 && (
                                <div className="mt-6 pt-6 border-t border-indigo-800">
                                    <h4 className="text-sm font-semibold text-red-300 mb-2 uppercase tracking-wide">System Warnings</h4>
                                    <ul className="space-y-2">
                                        {data.errors.map((err, i) => (
                                            <li key={i} className="text-xs text-indigo-200 flex gap-2">
                                                <X size={14} className="mt-0.5 shrink-0" />
                                                {typeof err === 'string' ? err : JSON.stringify(err)}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </div>
        )}
      </main>
    </div>
  );
}