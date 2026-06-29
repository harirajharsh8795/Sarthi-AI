import React, { useState } from "react";
import { Plus, Sun, Moon, FileText, BarChart3, ChevronDown, ChevronUp, Brain } from "lucide-react";
import SearchPanel from "../sidebar/SearchPanel";
import ConversationList from "../ConversationList";
import DocumentPanel from "../sidebar/DocumentPanel";
import SystemStats from "../sidebar/SystemStats";
import { translations } from "../../utils/localization";

export default function Sidebar({
  conversations,
  activeConversationId,
  onConversationClick,
  onNewChat,
  onDeleteConversation,
  onRenameConversation,
  sessionId,
  conversationId,
  refreshTrigger,
  language,
  setLanguage,
  theme,
  toggleTheme,
  documentsList,
  onBackToLanding
}) {
  const t = translations[language] || translations.en;

  const [docsExpanded, setDocsExpanded] = useState(true);
  const [statsExpanded, setStatsExpanded] = useState(false);

  return (
    <aside
      className="w-[280px] border-r flex flex-col h-full flex-shrink-0 select-none z-10 animate-fade-in"
      style={{
        background: "var(--bg-secondary)",
        borderColor: "var(--border)"
      }}
    >
      {/* 1. Logo Header */}
      <div 
        onClick={onBackToLanding}
        className="p-4 flex items-center justify-between border-b cursor-pointer hover:bg-white/[0.03] transition group" 
        style={{ borderColor: "var(--border)" }}
        title="Back to Landing Page"
      >
        <div className="flex items-center gap-2">
          <div
            className="w-7 h-7 rounded-lg flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform"
            style={{ background: "var(--accent-gradient)" }}
          >
            <Brain className="w-4 h-4 text-white" />
          </div>
          <span className="text-xs font-black tracking-tight text-gradient">
            {t.appTitle}
          </span>
        </div>
        <span className="badge badge-success text-[8px] font-bold">
          {language === "hi" ? "ऑफलाइन" : "Offline"}
        </span>
      </div>

      {/* 2. Actions (New Chat) */}
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="btn-primary w-full py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 cursor-pointer border-none text-white text-xs font-bold transition shadow"
        >
          <Plus size={14} />
          <span>{t.newChat}</span>
        </button>
      </div>

      {/* 3. Global Search Panel */}
      <div className="px-3 pb-2 border-b" style={{ borderColor: "var(--border)" }}>
        <SearchPanel
          language={language}
          conversations={conversations}
          onConversationClick={onConversationClick}
          sessionId={sessionId}
          documentsList={documentsList}
        />
      </div>

      {/* 4. Conversations List (scrollable area) */}
      <div className="flex-1 overflow-y-auto">
        <ConversationList
          conversations={conversations}
          activeConversationId={activeConversationId}
          onConversationClick={onConversationClick}
          onDeleteConversation={onDeleteConversation}
          onRenameConversation={onRenameConversation}
          language={language}
        />
      </div>

      {/* 5. Collapsible bottom utilities */}
      <div className="p-3 border-t space-y-2" style={{ borderColor: "var(--border)" }}>
        {/* Documents Collapsible Manager */}
        <div className="rounded-xl overflow-hidden border" style={{ borderColor: "var(--border)" }}>
          <button
            onClick={() => setDocsExpanded(!docsExpanded)}
            className="w-full px-3 py-2 flex justify-between items-center bg-white/5 hover:bg-white/10 transition text-xs font-semibold cursor-pointer border-none"
            style={{ color: "var(--text-primary)" }}
          >
            <span className="flex items-center gap-2">
              <FileText size={14} className="text-purple-500" />
              <span>{t.documentsHeader}</span>
            </span>
            <span className="text-[10px] text-slate-500 font-bold">
              {docsExpanded ? "▲" : "▼"}
            </span>
          </button>
          {docsExpanded && (
            <div className="p-2 border-t" style={{ borderColor: "var(--border)", background: "var(--bg-primary)" }}>
              <DocumentPanel
                sessionId={sessionId}
                conversationId={conversationId}
                refreshTrigger={refreshTrigger}
                language={language}
              />
            </div>
          )}
        </div>

        {/* System telemetry stats collapsible */}
        <SystemStats
          sessionId={sessionId}
          conversationId={conversationId}
          documentsCount={documentsList ? documentsList.length : 0}
          language={language}
        />
      </div>

      {/* 6. Sticky Footer */}
      <div className="p-3 border-t flex items-center justify-between" style={{ borderColor: "var(--border)" }}>
        {/* Language switcher segment */}
        <div className="sidebar-tab-wrapper flex-shrink-0" style={{ width: "90px" }}>
          <button
            onClick={() => setLanguage("en")}
            className={`sidebar-tab-btn ${language === "en" ? "active" : ""}`}
          >
            EN
          </button>
          <button
            onClick={() => setLanguage("hi")}
            className={`sidebar-tab-btn ${language === "hi" ? "active" : ""}`}
          >
            हिं
          </button>
        </div>

        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-xl hover:bg-[var(--surface-hover)] cursor-pointer border-none bg-transparent transition"
          style={{ color: "var(--text-secondary)" }}
          title={theme === "dark" ? t.lightMode : t.darkMode}
        >
          {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
        </button>
      </div>
    </aside>
  );
}
