import React, { useState, useEffect } from "react";
import { BarChart3, Wifi, Cpu, Database, Compass, FileText, Zap } from "lucide-react";
import { translations } from "../../utils/localization";

const API_BASE = "http://localhost:8000";

export default function SystemStats({ sessionId, conversationId, documentsCount, language }) {
  const t = translations[language] || translations.en;
  
  const [expanded, setExpanded] = useState(false);
  const [health, setHealth] = useState(null);
  const [telemetry, setTelemetry] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStats = async () => {
    setLoading(true);
    try {
      // 1. Fetch backend health (Ollama status, KB chunks, etc.)
      const healthRes = await fetch(`${API_BASE}/api/health`);
      if (healthRes.ok) {
        const healthData = await healthRes.ok ? await healthRes.json() : null;
        setHealth(healthData);
      }

      // 2. Fetch telemetry averages
      const telemetryRes = await fetch(`${API_BASE}/api/telemetry`);
      if (telemetryRes.ok) {
        const telemetryData = await telemetryRes.json();
        setTelemetry(telemetryData);
      }
    } catch (err) {
      console.error("Failed to fetch system status:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let interval = null;
    if (expanded) {
      fetchStats();
      interval = setInterval(() => {
        fetchStats();
      }, 10000); // 10s auto-refresh
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [expanded]);

  return (
    <div className="flex flex-col rounded-xl overflow-hidden border" style={{ borderColor: "var(--border)" }}>
      {/* Header Button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-3 py-2 flex justify-between items-center bg-white/5 hover:bg-white/10 transition text-xs font-semibold cursor-pointer border-none"
        style={{ color: "var(--text-primary)" }}
      >
        <span className="flex items-center gap-2">
          <BarChart3 size={14} className="text-purple-500" />
          <span>{t.systemLabel || "System"}</span>
        </span>
        <span className="text-[10px] text-slate-500 font-bold">{expanded ? "▲" : "▼"}</span>
      </button>

      {expanded && (
        <div className="p-3 bg-white/2 border-t flex flex-col space-y-3" style={{ borderColor: "var(--border)" }}>
          {loading && !health && (
            <div className="flex justify-center items-center py-4">
              <svg className="animate-spin h-4 w-4 text-purple-500" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          )}

          {/* status 2x3 grid */}
          <div className="grid grid-cols-2 gap-2 text-left">
            {/* Card 1: Offline status */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">Offline</span>
                <Wifi size={10} className="text-green-500" />
              </div>
              <span className="text-[9px] font-bold text-green-500 mt-1">{t.offlineMode}</span>
            </div>

            {/* Card 2: LLM status */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">LLM</span>
                <Cpu size={10} className={health?.ollama_status === "ok" ? "text-green-500" : "text-red-500"} />
              </div>
              <span className={`text-[9px] font-bold mt-1 ${
                health?.ollama_status === "ok" ? "text-green-500" : "text-red-500"
              }`}>
                {health?.ollama_status === "ok" ? t.llmReady : t.llmOffline}
              </span>
            </div>

            {/* Card 3: KB chunks */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">{t.kbChunks}</span>
                <Database size={10} className="text-purple-500" />
              </div>
              <span className="text-[10px] font-black text-slate-300 mt-1">
                {health?.kb_chunks || 0}
              </span>
            </div>

            {/* Card 4: Embed Model */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">{t.embeddingModel}</span>
                <Compass size={10} className="text-blue-500" />
              </div>
              <span className="text-[9px] font-bold text-slate-350 truncate mt-1" title={health?.embedding_model}>
                MPNet-v2
              </span>
            </div>

            {/* Card 5: Current docs */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">{t.documentsCount}</span>
                <FileText size={10} className="text-yellow-500" />
              </div>
              <span className="text-[10px] font-black text-slate-300 mt-1">
                {documentsCount}
              </span>
            </div>

            {/* Card 6: Average Latency */}
            <div className="card p-2 flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <span className="text-[8px] font-bold text-slate-500 uppercase">{t.avgLatency}</span>
                <Zap size={10} className="text-orange-500 animate-pulse" />
              </div>
              <span className="text-[9px] font-bold text-slate-300 mt-1">
                {telemetry?.summary?.avg_generation_time_ms 
                  ? `${Math.round(telemetry.summary.avg_generation_time_ms)}ms` 
                  : "0ms"}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
