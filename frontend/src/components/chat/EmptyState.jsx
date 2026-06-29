import React from "react";
import SuggestionCards from "./SuggestionCards";
import { translations } from "../../utils/localization";
import { FileText, Brain } from "lucide-react";

export default function EmptyState({ language, onSuggestionClick, recentDocs }) {
  const t = translations[language] || translations.en;

  return (
    <div className="flex flex-col items-center justify-center py-10 max-w-2xl mx-auto space-y-8 select-none mt-6 text-center animate-fade-in">
      {/* Brand logo header */}
      <div className="relative">
        <div 
          className="w-16 h-16 rounded-2xl flex items-center justify-center text-white shadow-lg animate-pulse-glow"
          style={{ background: "var(--accent-gradient)" }}
        >
          <Brain className="w-8 h-8 text-white" />
        </div>
        <div 
          className="absolute -inset-1 rounded-2xl blur-xl opacity-30 pointer-events-none"
          style={{ background: "var(--accent-gradient)" }}
        />
      </div>

      <div className="space-y-3">
        <h2 className="text-2xl font-black tracking-tight text-gradient">
          {t.welcomeHeading}
        </h2>
        <p className="text-xs max-w-md mx-auto" style={{ color: "var(--text-secondary)" }}>
          {language === "hi" ? "दस्तावेज़ अपलोड करें या नीचे दिए गए विषयों के बारे में पूछें।" : "Upload a document, or ask anything about our specialized offline domains."}
        </p>
      </div>

      {/* Domain Suggestion Cards */}
      <div className="w-full">
        <SuggestionCards language={language} onSuggestionClick={onSuggestionClick} />
      </div>

      {/* Recent Uploads Section */}
      {recentDocs && recentDocs.length > 0 && (
        <div className="w-full pt-6 text-left border-t" style={{ borderColor: "var(--border)" }}>
          <h4 className="text-[10px] font-bold uppercase tracking-wider mb-3 flex items-center gap-1.5" style={{ color: "var(--text-muted)" }}>
            <FileText size={12} className="text-purple-500" />
            {t.recentUploads}
          </h4>
          <div className="flex flex-wrap gap-2">
            {recentDocs.slice(0, 3).map((doc) => (
              <button
                key={doc.document_id}
                onClick={() => onSuggestionClick(`@${doc.original_filename} `)}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer border-none glass glass-hover transition"
                style={{ color: "var(--text-secondary)" }}
              >
                <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                <span className="truncate max-w-[150px]">{doc.original_filename}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
