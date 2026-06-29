import React, { useEffect } from "react";
import { translations } from "../utils/localization";

export default function CitationDrawer({ citation, isOpen, onClose, language }) {
  const t = translations[language] || translations.en;

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!citation) return null;

  const isUserDoc = citation.collection === "user_docs";

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 transition-opacity"
          onClick={onClose}
        />
      )}
      <div
        className={`fixed inset-y-0 right-0 w-80 bg-[#05030F] shadow-2xl border-l border-white/[0.08] z-50 transform transition-transform duration-300 ease-in-out flex flex-col text-slate-300 ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/[0.06]">
          <div className="flex items-center space-x-2">
            <span className="bg-purple-500/20 text-purple-400 text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center border border-purple-500/30">
              {citation.index}
            </span>
            <h3 className="font-semibold text-slate-250 text-sm">{t.sourceTitle}</h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 transition p-1 rounded-lg hover:bg-white/[0.04] cursor-pointer border-none bg-transparent"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-left">
          {/* Metadata section */}
          <div>
            <h4 className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
              {t.metadata}
            </h4>
            <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-3 space-y-2.5 text-xs">
              <div>
                <span className="text-slate-500 block text-[10px] uppercase">{t.fileName}</span>
                <span className="text-slate-300 font-medium break-all">{citation.filename || "Unknown"}</span>
              </div>
              {citation.page_label && (
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">{t.pageNumber}</span>
                  <span className="text-slate-300 font-medium">Page {citation.page_label}</span>
                </div>
              )}
              <div>
                <span className="text-slate-500 block text-[10px] uppercase">{t.category}</span>
                <span className="text-slate-300 font-medium capitalize">{citation.domain}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px] uppercase">{t.sourceOrigin}</span>
                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold mt-1 ${
                  isUserDoc
                    ? "bg-purple-950/40 text-purple-300 border border-purple-500/20"
                    : "bg-blue-950/40 text-blue-300 border border-blue-500/20"
                }`}>
                  {isUserDoc ? t.userDoc : t.publicKb}
                </span>
              </div>
            </div>
          </div>

          {/* Text Preview / Content section */}
          <div className="pt-2">
            <h4 className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
              {t.docExcerpt}
            </h4>
            {isUserDoc ? (
              <div className="bg-purple-950/20 border border-purple-900/40 rounded-xl p-4 text-center">
                <svg className="w-8 h-8 text-purple-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <p className="text-xs text-purple-300 font-semibold">{t.userDoc}</p>
                <p className="text-[10px] text-purple-450 mt-1">{t.docPrivate}</p>
              </div>
            ) : (
              <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-3.5 text-xs text-slate-300 leading-relaxed shadow-md italic">
                "{citation.text_preview || "No preview available."}..."
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
