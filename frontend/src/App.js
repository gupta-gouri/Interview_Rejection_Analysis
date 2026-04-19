import React, { useState, useEffect, useRef } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Upload, FileAudio, Activity, BrainCircuit, CheckCircle, AlertCircle } from 'lucide-react';

const defaultTimelineData = [
  { time: '0:00', score: 80 },
  { time: '1:00', score: 85 },
  { time: '2:00', score: 70 },
  { time: '3:00', score: 40 },
  { time: '4:00', score: 65 },
  { time: '5:00', score: 55 },
  { time: '6:00', score: 75 },
  { time: '7:00', score: 90 },
];

const processingSteps = [
  "Initializing AI engines...",
  "Transcribing audio...",
  "Analyzing speech patterns & STAR method...",
  "Generating report..."
];

function App() {
  const [appState, setAppState] = useState('upload'); // 'upload', 'processing', 'dashboard'
  const [stepIndex, setStepIndex] = useState(0);

  // Form State
  const [selectedFile, setSelectedFile] = useState(null);
  const [role, setRole] = useState('SDE');
  const [experienceLevel, setExperienceLevel] = useState('Mid-Level');
  
  // Results State
  const [analysisResults, setAnalysisResults] = useState(null);
  
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("Please select an audio file first.");
      return;
    }
    
    setAppState('processing');
    setStepIndex(0);

    // Simulate progress steps while waiting for the real API
    const interval = setInterval(() => {
      setStepIndex((prev) => (prev < 2 ? prev + 1 : prev));
    }, 4000); // Progress slowly while waiting for backend

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("role", role);
      formData.append("experience_level", experienceLevel);

      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze interview");
      }

      const data = await response.json();
      setAnalysisResults(data);
      
      clearInterval(interval);
      setStepIndex(3); // "Generating report..."
      
      setTimeout(() => {
        setAppState('dashboard');
      }, 1000);

    } catch (error) {
      console.error("Error analyzing:", error);
      alert("An error occurred during analysis. Make sure the backend is running.");
      clearInterval(interval);
      setAppState('upload');
    }
  };

  // Mapped Data for Dashboard
  const dynamicScores = analysisResults ? [
    { label: "Clarity", value: analysisResults.llm_scores?.clarity_score ? Math.round((analysisResults.llm_scores.clarity_score / 5) * 100) : 0, trend: "AI Score", color: "text-blue-400" },
    { label: "Depth", value: analysisResults.llm_scores?.depth_score ? Math.round((analysisResults.llm_scores.depth_score / 5) * 100) : 0, trend: "AI Score", color: "text-indigo-400" },
    { label: "Structure", value: analysisResults.llm_scores?.structure_score ? Math.round((analysisResults.llm_scores.structure_score / 5) * 100) : 0, trend: "STAR", color: "text-red-400" },
    { label: "Overall Weighted", value: analysisResults.final_result?.final_score ? Math.round((analysisResults.final_result.final_score / 5) * 100) : 0, trend: role, color: "text-emerald-400" },
  ] : [];

  const dynamicHeatmapData = analysisResults?.weaknesses ? analysisResults.weaknesses.map((w, i) => {
    // Determine issue text based on severity
    let issueText = null;
    if (w.severity > 0.6) issueText = "Critical Gap";
    else if (w.severity > 0.3) issueText = "Needs Improvement";
    else if (w.severity > 0) issueText = "Minor Issue";
    
    return {
      id: i,
      question: w.id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      score: Math.max(10, Math.round(100 - (w.severity * 100))), // Base score on severity
      issue: issueText
    };
  }) : [];

  const dynamicRecommendations = analysisResults?.star_result?.suggestions ? analysisResults.star_result.suggestions.map(s => ({
    title: "STAR Framework Tip",
    desc: s,
    type: "structure"
  })) : [];
  
  // Add some fallback recommendations if none were found
  if (dynamicRecommendations.length === 0 && analysisResults?.speech_metrics?.hesitation_score > 0.3) {
      dynamicRecommendations.push({
          title: "Speech Delivery",
          desc: `High hesitation detected. Try taking a 1-second pause before answering instead of using fillers.`,
          type: "speech"
      });
  }

  const timelineData = analysisResults?.segments ? analysisResults.segments.map((seg, idx) => ({
      time: seg.start,
      // Create a pseudo-score to visualize timeline fluctuations (since we don't have per-segment scores yet)
      score: 50 + (Math.random() * 40)
  })) : defaultTimelineData;


  if (appState === 'upload') {
    return (
      <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
        {/* Abstract Backgrounds */}
        <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[100px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[100px]" />
        
        <div className="glass-panel max-w-xl w-full p-10 rounded-3xl relative z-10 flex flex-col items-center">
          <div className="w-20 h-20 bg-blue-500/10 rounded-full flex items-center justify-center mb-6 animate-float">
            <Upload size={36} className="text-blue-400" />
          </div>
          <h1 className="text-4xl font-extrabold mb-3 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500 text-center">
            Upload Interview
          </h1>
          <p className="text-gray-400 mb-10 text-center text-sm px-4">
            Our AI will analyze your audio for confidence, clarity, and depth to provide actionable feedback.
          </p>
          
          <div className="w-full space-y-6">
            <div 
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-white/20 rounded-2xl p-10 text-center hover:border-blue-500/50 hover:bg-white/5 transition-all cursor-pointer group"
            >
              <FileAudio size={40} className="mx-auto text-gray-500 mb-4 group-hover:text-blue-400 transition-colors" />
              <p className="text-base text-gray-300 font-medium">
                {selectedFile ? selectedFile.name : "Click to select your audio file"}
              </p>
              <p className="text-xs text-gray-500 mt-2">MP3, WAV up to 50MB</p>
              <input 
                type="file" 
                className="hidden" 
                ref={fileInputRef} 
                accept="audio/*" 
                onChange={handleFileChange} 
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-400">Target Role</label>
                  <select 
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none text-sm"
                  >
                    <option className="bg-[#050505] text-white">SDE</option>
                    <option className="bg-[#050505] text-white">HR</option>
                    <option className="bg-[#050505] text-white">Analyst</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-400">Experience Level</label>
                  <select 
                    value={experienceLevel}
                    onChange={(e) => setExperienceLevel(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none text-sm"
                  >
                    <option className="bg-[#050505] text-white">Junior</option>
                    <option className="bg-[#050505] text-white">Mid-Level</option>
                    <option className="bg-[#050505] text-white">Senior</option>
                  </select>
                </div>
            </div>
            
            <button 
              onClick={handleAnalyze}
              className={`w-full font-semibold py-4 rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] transition-all active:scale-[0.98] mt-4 ${selectedFile ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white' : 'bg-gray-800 text-gray-500 cursor-not-allowed'}`}
              disabled={!selectedFile}
            >
              Analyze Interview
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (appState === 'processing') {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">
        <div className="relative w-48 h-48 flex items-center justify-center mb-10">
          <div className="absolute inset-0 border-[3px] border-blue-500/20 rounded-full"></div>
          <div className="absolute inset-0 border-[3px] border-blue-500 rounded-full border-t-transparent animate-spin duration-1000"></div>
          <div className="absolute inset-0 bg-blue-500/10 rounded-full animate-pulse-ring"></div>
          <BrainCircuit size={48} className="text-blue-400 animate-pulse" />
        </div>
        <h2 className="text-3xl font-bold text-white tracking-wide mb-8 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">
          Processing Interview
        </h2>
        <div className="flex flex-col items-center space-y-4">
          {processingSteps.map((step, idx) => (
            <div 
              key={idx} 
              className={`text-base transition-all duration-700 ease-out flex items-center
                ${idx === stepIndex ? 'text-blue-400 font-medium scale-110 translate-x-2' : 
                  idx < stepIndex ? 'text-gray-600 translate-x-0' : 'text-gray-800 translate-x-0'}`}
            >
              {idx < stepIndex && <CheckCircle size={14} className="mr-2 text-emerald-500" />}
              {idx === stepIndex && <Activity size={14} className="mr-2 animate-pulse" />}
              {step}
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 md:p-8 lg:p-10 max-w-7xl mx-auto">
      <header className="mb-10 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-full text-xs font-semibold mb-4">
            <Activity size={14} />
            <span>Analysis Complete</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            Interview Dashboard
          </h1>
          <p className="text-gray-400 mt-2 text-sm font-medium">Role: {analysisResults?.role} • Experience: {analysisResults?.experience_level}</p>
        </div>
        <button 
          onClick={() => {
            setAppState('upload');
            setSelectedFile(null);
            setAnalysisResults(null);
          }} 
          className="text-sm font-medium text-gray-300 hover:text-white transition-all border border-white/10 px-5 py-2.5 rounded-xl hover:bg-white/10 active:scale-95 flex items-center"
        >
          <Upload size={16} className="mr-2" /> New Analysis
        </button>
      </header>
      
      {/* Scorecards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
        {dynamicScores.map((score, i) => (
          <div key={i} className="glass-panel p-6 rounded-3xl relative overflow-hidden group hover:border-white/20 transition-all">
            <div className={`absolute top-0 left-0 w-1 h-full ${score.color.replace('text-', 'bg-')}`}></div>
            <h3 className="text-gray-400 font-medium text-sm mb-3">{score.label}</h3>
            <div className="flex items-end justify-between">
              <p className="text-4xl font-extrabold tracking-tight text-white">{score.value}<span className="text-xl text-gray-500 font-semibold">%</span></p>
              <span className={`text-xs font-bold px-2.5 py-1 rounded-md bg-white/5 text-gray-400`}>
                {score.trend}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
        {/* Main Analysis Area */}
        <div className="lg:col-span-2 space-y-6 md:space-y-8">
          
          {/* Timeline Chart */}
          <div className="glass-panel p-6 md:p-8 rounded-3xl">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-xl font-bold flex items-center text-white"><Activity className="mr-3 text-blue-400" size={22}/> Confidence Timeline (Simulated)</h2>
            </div>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" vertical={false} />
                  <XAxis dataKey="time" stroke="#ffffff40" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#9ca3af'}} dy={10} />
                  <YAxis stroke="#ffffff40" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#9ca3af'}} domain={[0, 100]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', color: '#fff', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}
                    itemStyle={{ color: '#60A5FA', fontWeight: 'bold' }}
                  />
                  <Area type="monotone" dataKey="score" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Question Breakdown Heatmap */}
          <div className="glass-panel p-6 md:p-8 rounded-3xl">
            <h2 className="text-xl font-bold mb-8 flex items-center text-white"><AlertCircle className="mr-3 text-indigo-400" size={22}/> Weakness Analyzer</h2>
            <div className="space-y-4">
              {dynamicHeatmapData.length > 0 ? dynamicHeatmapData.map((item) => (
                <div key={item.id} className="group flex flex-col sm:flex-row sm:items-center gap-4 p-4 rounded-2xl bg-white/[0.02] border border-white/[0.04] hover:bg-white/[0.06] transition-all">
                  <div className="sm:w-1/3 text-sm text-gray-200 font-medium tracking-wide">{item.question}</div>
                  <div className="flex-1 h-2.5 bg-black/40 rounded-full overflow-hidden flex shadow-inner">
                    <div 
                      className={`h-full transition-all duration-1000 ease-out ${
                        item.score > 75 ? 'bg-gradient-to-r from-emerald-500 to-emerald-300' : 
                        item.score > 50 ? 'bg-gradient-to-r from-yellow-500 to-yellow-300' : 
                        'bg-gradient-to-r from-red-500 to-red-400'
                      }`}
                      style={{ width: `${item.score}%` }}
                    />
                  </div>
                  <div className="sm:w-1/4 text-right text-xs font-semibold">
                    {item.issue ? 
                      <span className={`inline-flex items-center px-2.5 py-1.5 rounded-lg border shadow-sm ${item.issue === 'Critical Gap' ? 'text-red-400 bg-red-400/10 border-red-400/20' : 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20'}`}><AlertCircle size={14} className="mr-1.5"/>{item.issue}</span> : 
                      <span className="inline-flex items-center text-emerald-400 bg-emerald-400/10 px-2.5 py-1.5 rounded-lg border border-emerald-400/20 shadow-sm"><CheckCircle size={14} className="mr-1.5"/>Clear</span>
                    }
                  </div>
                </div>
              )) : (
                <div className="text-center text-gray-500 py-4">No critical weaknesses detected!</div>
              )}
            </div>
          </div>

        </div>

        {/* Sidebar */}
        <div className="space-y-6 md:space-y-8">
          
          {/* Actionable Feedback */}
          <div className="glass-panel p-6 md:p-8 rounded-3xl">
            <h2 className="text-xl font-bold mb-8 flex items-center text-white"><BrainCircuit className="mr-3 text-emerald-400" size={22}/> Actionable Feedback</h2>
            <div className="space-y-6">
              {dynamicRecommendations.length > 0 ? dynamicRecommendations.map((rec, index) => (
                <div key={index} className="relative pl-7 before:absolute before:left-0 before:top-1.5 before:w-2.5 before:h-2.5 before:bg-gradient-to-b before:from-blue-400 before:to-indigo-500 before:rounded-full before:shadow-[0_0_10px_rgba(59,130,246,0.8)]">
                  <h4 className="text-sm font-bold text-gray-100 mb-1.5">{rec.title}</h4>
                  <p className="text-xs text-gray-400 leading-relaxed font-medium">{rec.desc}</p>
                </div>
              )) : (
                 <p className="text-sm text-gray-400 italic">No specific recommendations at this time.</p>
              )}
            </div>
          </div>

          {/* Speech Metrics Checklist */}
          <div className="glass-panel p-6 md:p-8 rounded-3xl bg-gradient-to-b from-white/[0.03] to-transparent">
            <h3 className="text-base font-bold text-gray-200 mb-6 flex items-center"><Activity size={18} className="mr-2 text-blue-400"/> Speech Metrics</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between text-sm text-gray-300 font-medium">
                  <span>Filler Word Count</span>
                  <span className="text-white font-bold">{analysisResults?.speech_metrics?.filler_count || 0}</span>
              </div>
              <div className="flex items-center justify-between text-sm text-gray-300 font-medium">
                  <span>Speech Speed (WPM)</span>
                  <span className="text-white font-bold">{analysisResults?.speech_metrics?.speech_speed || 0}</span>
              </div>
              <div className="flex items-center justify-between text-sm text-gray-300 font-medium">
                  <span>Avg Pause Duration</span>
                  <span className="text-white font-bold">{analysisResults?.speech_metrics?.avg_pause_duration || 0}s</span>
              </div>
              <div className="flex items-center justify-between text-sm text-gray-300 font-medium">
                  <span>STAR Components Found</span>
                  <span className="text-emerald-400 font-bold">{Object.values(analysisResults?.star_result?.components_found || {}).filter(Boolean).length || 0}/4</span>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}

export default App;