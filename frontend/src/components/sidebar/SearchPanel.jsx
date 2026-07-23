import React, { useState, useEffect, useRef } from "react";
import { Search, MessageSquare, FileText, ChevronRight } from "lucide-react";
import { translations } from "../../utils/localization";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function SearchPanel({ 
  language, 
  conversations, 
  onConversationClick, 
  sessionId, 
  documentsList 
}) {
  const t = translations[language] || translations.en;
  
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState("convs"); // "convs" | "msgs" | "docs"
  const [msgResults, setMsgResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef(null);

  // Debounced search for messages backend endpoint
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    
    if (!query.trim()) {
      setMsgResults([]);
      return;
    }

    if (activeTab === "msgs") {
      setLoading(true);
      debounceRef.current = setTimeout(async () => {
        try {
          const response = await fetch(`${API_BASE}/api/search/messages?session_id=${sessionId}&q=${encodeURIComponent(query)}`);
          if (response.ok) {
            const data = await response.json();
            setMsgResults(data.results || []);
          }
        } catch (err) {
          console.error("Search messages failed:", err);
        } finally {
          setLoading(false);
        }
      }, 300);
    }
  }, [query, activeTab, sessionId]);

  // Client-side search filters
  const filteredConvs = conversations.filter((c) =>
    (c.title || "").toLowerCase().includes(query.toLowerCase())
  );

  const filteredDocs = documentsList
    ? documentsList.filter((d) =>
        (d.original_filename || "").toLowerCase().includes(query.toLowerCase())
      )
    : [];

  return (
    <div className="flex flex-col space-y-3 w-full animate-fade-in p-1">
      {/* Search Input */}
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t.searchPlaceholder || "Search..."}
          className="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl input-surface focus-ring"
        />
        <Search size={14} className="absolute left-2.5 top-2.5 text-slate-500" />
      </div>

      {/* Tabs list */}
      <div className="sidebar-tab-wrapper">
        <button
          onClick={() => setActiveTab("convs")}
          className={`sidebar-tab-btn ${activeTab === "convs" ? "active" : ""}`}
        >
          {t.searchConversations}
        </button>
        <button
          onClick={() => setActiveTab("msgs")}
          className={`sidebar-tab-btn ${activeTab === "msgs" ? "active" : ""}`}
        >
          {t.searchMessages}
        </button>
        <button
          onClick={() => setActiveTab("docs")}
          className={`sidebar-tab-btn ${activeTab === "docs" ? "active" : ""}`}
        >
          {t.searchDocuments}
        </button>
      </div>

      {/* Results Container */}
      <div className="max-h-48 overflow-y-auto custom-scrollbar flex flex-col space-y-1 pr-1">
        {/* TAB 1: Conversations */}
        {activeTab === "convs" && (
          filteredConvs.length === 0 ? (
            <span className="text-[10px] text-center text-slate-500 py-3">{t.noResults}</span>
          ) : (
            filteredConvs.map((c) => (
              <button
                key={c.id}
                onClick={() => onConversationClick(c.id)}
                className="search-result-item"
              >
                <div className="flex items-center gap-2 truncate">
                  <MessageSquare size={12} className="text-purple-500 flex-shrink-0" />
                  <span className="truncate">{c.title || "Untitled Chat"}</span>
                </div>
                <ChevronRight size={10} className="text-slate-500" />
              </button>
            ))
          )
        )}

        {/* TAB 2: Messages */}
        {activeTab === "msgs" && (
          loading ? (
            <span className="text-[10px] text-center text-slate-500 py-3">Searching...</span>
          ) : msgResults.length === 0 ? (
            <span className="text-[10px] text-center text-slate-500 py-3">{t.noResults}</span>
          ) : (
            msgResults.map((r) => (
              <button
                key={r.message_id}
                onClick={() => onConversationClick(r.conversation_id)}
                className="search-result-card"
              >
                <div className="flex items-center justify-between w-full">
                  <span className="text-[9px] font-bold text-purple-500 truncate max-w-[120px]">
                    {r.title}
                  </span>
                  <span className="text-[8px] text-slate-500">{r.role}</span>
                </div>
                <p className="text-[10px] line-clamp-2 leading-relaxed text-slate-400 italic">
                  "{r.snippet}..."
                </p>
              </button>
            ))
          )
        )}

        {/* TAB 3: Documents */}
        {activeTab === "docs" && (
          filteredDocs.length === 0 ? (
            <span className="text-[10px] text-center text-slate-500 py-3">{t.noResults}</span>
          ) : (
            filteredDocs.map((d) => (
              <div
                key={d.document_id}
                className="search-result-item pointer-events-none"
              >
                <div className="flex items-center gap-2 truncate">
                  <FileText size={12} className="text-purple-500 flex-shrink-0" />
                  <span className="truncate">{d.original_filename}</span>
                </div>
                <span className="text-[9px] opacity-75">{d.file_type}</span>
              </div>
            ))
          )
        )}
      </div>
    </div>
  );
}
