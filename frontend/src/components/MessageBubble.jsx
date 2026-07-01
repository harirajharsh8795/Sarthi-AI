import React, { useState, useRef, useEffect } from "react";
import { 
  Edit3, Trash2, RotateCw, Copy, Check, FileText, ThumbsUp, ThumbsDown, Volume2, Square,
  CheckCircle2, AlertTriangle, AlertCircle, Brain
} from "lucide-react";
import { translations } from "../../utils/localization";

const API_BASE = "http://localhost:8000";

export default function MessageBubble({ 
  message, 
  onCitationClick, 
  language, 
  onDelete, 
  onEdit, 
  onRegenerate, 
  index, 
  isLast 
}) {
  const t = translations[language] || translations.en;
  const isUser = message.role === "user";
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [speakingLoading, setSpeakingLoading] = useState(false);
  const [sourcesExpanded, setSourcesExpanded] = useState(false);
  const [copiedType, setCopiedType] = useState(null); // "md" or "text" or "export"
  const [feedback, setFeedback] = useState(null); // "up" or "down"
  const [isEditing, setIsEditing] = useState(false);
  const [editVal, setEditVal] = useState(message.content);
  
  const audioRef = useRef(null);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        if (audioRef.current.src) {
          URL.revokeObjectURL(audioRef.current.src);
        }
      }
    };
  }, []);

  // Simple token estimator: ~1.3 tokens per word
  const estimateTokens = () => {
    if (!message.content) return 0;
    const words = message.content.trim().split(/\s+/).length;
    return Math.round(words * 1.35);
  };

  const getConfidenceIndicator = () => {
    if (isUser) return null;
    
    const isFallback = 
      message.content?.startsWith("I could not find") || 
      message.content?.startsWith("मुझे इस विषय") ||
      message.content?.includes("not found in the uploaded");
      
    if (isFallback) {
      return {
        variant: "danger",
        icon: AlertCircle,
        label: t.notFound || "Not found"
      };
    }
    
    if (message.citations && message.citations.length > 0) {
      return {
        variant: "success",
        icon: CheckCircle2,
        label: t.verified || "Verified"
      };
    }
    
    return {
      variant: "warning",
      icon: AlertTriangle,
      label: t.noSources || "No sources"
    };
  };

  const handleSpeak = async () => {
    if (isPlaying) {
      if (audioRef.current) {
        audioRef.current.pause();
        if (audioRef.current.src) {
          URL.revokeObjectURL(audioRef.current.src);
        }
        audioRef.current = null;
      }
      setIsPlaying(false);
      return;
    }

    setSpeakingLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/voice/speak`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: message.content.replace(/\[\d+\]/g, ""), // strip inline citations
          language: message.response_language || (language === "hi" ? "Hindi" : "English"),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to synthesize speech");
      }

      const blob = await response.blob();
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      
      audio.onended = () => {
        setIsPlaying(false);
        audioRef.current = null;
        URL.revokeObjectURL(audioUrl);
      };
      
      await audio.play();
      setIsPlaying(true);
    } catch (err) {
      console.error("TTS playback error:", err);
    } finally {
      setSpeakingLoading(false);
    }
  };

  const copyToClipboard = (type) => {
    let textToCopy = message.content;
    if (type === "text") {
      // Strip basic markdown syntax
      textToCopy = message.content
        .replace(/\*\*([^*]+)\*\*/g, "$1")
        .replace(/^-\s+/gm, "")
        .replace(/^\d+\.\s+/gm, "");
    }
    
    navigator.clipboard.writeText(textToCopy);
    setCopiedType(type);
    setTimeout(() => setCopiedType(null), 2000);
  };

  const exportResponse = () => {
    const blob = new Blob([message.content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `saarthi_response_${index + 1}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setCopiedType("export");
    setTimeout(() => setCopiedType(null), 2000);
  };

  const handleEditSubmit = () => {
    if (editVal.trim() && editVal !== message.content) {
      onEdit(index, editVal);
      setIsEditing(false);
    }
  };

  const formatText = (text) => {
    if (!text) return "";

    const lines = text.split("\n");
    return lines.map((line, lineIdx) => {
      const trimmed = line.trim();
      const isH2 = trimmed.startsWith("## ");
      const isH3 = trimmed.startsWith("### ");
      const isBullet = trimmed.startsWith("- ") || trimmed.startsWith("* ");
      const numberedMatch = trimmed.match(/^(\d+)\.\s+/);
      const isNumbered = !!numberedMatch;
      
      let content = line;
      if (isH2) content = trimmed.substring(3);
      else if (isH3) content = trimmed.substring(4);
      else if (isBullet) content = line.replace(/^[\s-*]+/, "");
      else if (isNumbered) content = line.replace(/^\s*\d+\.\s+/, "");

      // Markdown bold matching
      const boldRegex = /\*\*([^*]+)\*\*/g;
      const parts = [];
      let lastIndex = 0;
      let match;

      while ((match = boldRegex.exec(content)) !== null) {
        if (match.index > lastIndex) {
          parts.push(content.substring(lastIndex, match.index));
        }
        parts.push(
          <strong key={match.index} className="font-bold" style={{ color: "var(--text-primary)" }}>
            {match[1]}
          </strong>
        );
        lastIndex = boldRegex.lastIndex;
      }

      if (lastIndex < content.length) {
        parts.push(content.substring(lastIndex));
      }

      const inlineContent = parts.length > 0 ? parts : content;

      if (isH2) {
        return (
          <h2 key={lineIdx} className="text-base font-bold mt-4 mb-2" style={{ color: "var(--text-primary)" }}>
            {inlineContent}
          </h2>
        );
      }
      if (isH3) {
        return (
          <h3 key={lineIdx} className="text-sm font-bold mt-3 mb-1.5" style={{ color: "var(--text-primary)" }}>
            {inlineContent}
          </h3>
        );
      }
      if (isBullet) {
        return (
          <li key={lineIdx} className="ml-4 list-disc pl-1 mb-1" style={{ color: "var(--text-secondary)" }}>
            {inlineContent}
          </li>
        );
      }
      if (isNumbered) {
        return (
          <li key={lineIdx} style={{ listStyleType: 'decimal' }} className="ml-5 pl-1 mb-1" style={{ color: "var(--text-secondary)" }}>
            {inlineContent}
          </li>
        );
      }
      if (trimmed === "Sources:") {
        return null;
      }
      return (
        <p key={lineIdx} className={`mb-2 text-xs leading-relaxed ${trimmed === "" ? "h-2" : ""}`} style={{ color: "var(--text-secondary)" }}>
          {inlineContent}
        </p>
      );
    });
  };

  const indicator = getConfidenceIndicator();
  const ConfidenceIcon = indicator?.icon;

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-6 group relative`}>
      {/* Bot Avatar */}
      {!isUser && (
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mr-3 shadow-md select-none"
          style={{ background: "var(--accent-gradient)", color: "white" }}
        >
          <Brain className="w-4 h-4 text-white" />
        </div>
      )}

      {/* Bubble Shell */}
      <div
        className={`relative ${
          isUser
            ? "px-4 py-3 text-xs rounded-2xl rounded-tr-none text-left shadow-md max-w-[70%]"
            : "text-left pr-2 max-w-[calc(100%-44px)] flex-1"
        }`}
        style={{
          background: isUser ? "var(--user-bubble-bg)" : "transparent",
          color: isUser ? "white" : "var(--text-primary)",
        }}
      >
        {isEditing ? (
          <div className="space-y-2 w-full glass p-3 rounded-xl border">
            <textarea
              value={editVal}
              onChange={(e) => setEditVal(e.target.value)}
              className="w-full bg-transparent border-none text-xs focus:outline-none resize-none min-h-[60px]"
              style={{ color: "var(--text-primary)" }}
            />
            <div className="flex justify-end gap-2">
              <button 
                onClick={() => setIsEditing(false)} 
                className="px-3 py-1 rounded-lg text-[10px] cursor-pointer border-none bg-white/5"
                style={{ color: "var(--text-secondary)" }}
              >
                {t.cancel}
              </button>
              <button 
                onClick={handleEditSubmit} 
                className="px-3 py-1 rounded-lg text-[10px] cursor-pointer border-none bg-purple-600 text-white font-bold"
              >
                {t.confirmRename || "Save"}
              </button>
            </div>
          </div>
        ) : (
          <div>
            {/* Bubble Content */}
            {isUser ? (
              <p className="whitespace-pre-wrap text-xs leading-relaxed">{message.content}</p>
            ) : (
              <div className="space-y-2">
                <div>{formatText(message.content)}</div>

                {/* Sources section */}
                {message.citations && message.citations.length > 0 && (
                  <div className="mt-4 pt-3 border-t" style={{ borderColor: "var(--border)" }}>
                    <button
                      type="button"
                      onClick={() => setSourcesExpanded(!sourcesExpanded)}
                      className="flex items-center gap-1 text-[9px] font-bold text-slate-400 hover:text-slate-200 uppercase tracking-wider border-none bg-transparent cursor-pointer p-0"
                    >
                      <span>{t.sourcesToggle} ({message.citations.length})</span>
                      <span>{sourcesExpanded ? "▲" : "▼"}</span>
                    </button>

                    {sourcesExpanded && (
                      <ol className="mt-2 space-y-1 text-[11px] list-decimal pl-4" style={{ color: "var(--text-secondary)" }}>
                        {message.citations.map((cit) => (
                          <li key={cit.index}>
                            <span className="font-semibold">{cit.filename}</span>
                            <span className="text-[10px] opacity-70"> (Page {cit.page_number})</span>
                          </li>
                        ))}
                      </ol>
                    )}

                    {/* Quick Citation Pills */}
                    <div className="flex flex-wrap gap-1.5 mt-3.5">
                      {message.citations.map((cit) => (
                        <button
                          key={cit.index}
                          onClick={() => onCitationClick?.(cit)}
                          className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-medium cursor-pointer border-none glass glass-hover transition"
                          style={{ color: "var(--text-secondary)" }}
                        >
                          <span
                            className="text-[9px] w-3.5 h-3.5 rounded-full flex items-center justify-center font-bold"
                            style={{ background: "var(--accent-muted)", color: "var(--accent)" }}
                          >
                            {cit.index}
                          </span>
                          <span className="truncate max-w-[80px]">{cit.filename}</span>
                          <span className="text-[8px] opacity-60">P{cit.page_number}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Confidence indicator badge */}
                {indicator && (
                  <div className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wider border mt-2 ${
                    indicator.variant === "success"
                      ? "badge-success"
                      : indicator.variant === "warning"
                      ? "badge-warning"
                      : "badge-danger"
                  }`}>
                    <ConfidenceIcon size={10} />
                    <span>{indicator.label}</span>
                  </div>
                )}
              </div>
            )}

            {/* Bubble Action Bar (Fades in on hover) */}
            <div 
              className={`absolute top-0 right-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 ${
                isUser ? "-translate-y-full pb-1" : ""
              }`}
            >
              {isUser ? (
                <>
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-1 rounded-lg border border-white/10 bg-[#0A0718] hover:bg-white/5 text-slate-400 hover:text-purple-400 transition cursor-pointer"
                    title={t.editMessage}
                  >
                    <Edit3 size={11} />
                  </button>
                  <button
                    onClick={() => onDelete(index)}
                    className="p-1 rounded-lg border border-white/10 bg-[#0A0718] hover:bg-white/5 text-slate-400 hover:text-red-400 transition cursor-pointer"
                    title={t.deleteMessage}
                  >
                    <Trash2 size={11} />
                  </button>
                </>
              ) : (
                <div className="flex items-center gap-1 bg-[#0A0718] border border-white/10 p-0.5 rounded-lg shadow-lg">
                  {/* Speak answer */}
                  <button
                    onClick={handleSpeak}
                    disabled={speakingLoading}
                    className={`p-1 rounded transition cursor-pointer border-none bg-transparent ${
                      isPlaying ? "text-purple-400" : "text-slate-400 hover:text-purple-400"
                    }`}
                    title={isPlaying ? t.stopListen : t.listenBtn}
                  >
                    {speakingLoading ? (
                      <svg className="animate-spin h-3 w-3 text-slate-500" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                    ) : isPlaying ? (
                      <Square size={11} className="fill-current" />
                    ) : (
                      <Volume2 size={11} />
                    )}
                  </button>

                  {/* Copy Markdown */}
                  <button
                    onClick={() => copyToClipboard("md")}
                    className="p-1 rounded hover:bg-white/5 text-slate-400 hover:text-purple-400 border-none bg-transparent transition cursor-pointer"
                    title={t.copyMarkdown}
                  >
                    {copiedType === "md" ? <Check size={11} className="text-green-500" /> : <Copy size={11} />}
                  </button>

                  {/* Export */}
                  <button
                    onClick={exportResponse}
                    className="p-1 rounded hover:bg-white/5 text-slate-400 hover:text-purple-400 border-none bg-transparent transition cursor-pointer"
                    title={t.exportResponse}
                  >
                    {copiedType === "export" ? <Check size={11} className="text-green-500" /> : <FileText size={11} />}
                  </button>

                  {/* Feedback */}
                  <button
                    onClick={() => setFeedback("up")}
                    className={`p-1 rounded hover:bg-white/5 border-none bg-transparent transition cursor-pointer ${
                      feedback === "up" ? "text-green-500" : "text-slate-400 hover:text-green-400"
                    }`}
                    title={t.thumbsUp}
                  >
                    <ThumbsUp size={11} />
                  </button>
                  <button
                    onClick={() => setFeedback("down")}
                    className={`p-1 rounded hover:bg-white/5 border-none bg-transparent transition cursor-pointer ${
                      feedback === "down" ? "text-red-500" : "text-slate-400 hover:text-red-400"
                    }`}
                    title={t.thumbsDown}
                  >
                    <ThumbsDown size={11} />
                  </button>

                  {/* Estimated Token Badge */}
                  <span className="px-1.5 py-0.5 rounded text-[8px] font-mono text-slate-500 select-none">
                    ~{estimateTokens()} tokens
                  </span>

                  {/* Delete assistant bubble */}
                  <button
                    onClick={() => onDelete(index)}
                    className="p-1 rounded hover:bg-white/5 text-slate-400 hover:text-red-400 border-none bg-transparent transition cursor-pointer"
                    title={t.deleteMessage}
                  >
                    <Trash2 size={11} />
                  </button>
                </div>
              )}
            </div>

            {/* Regenerate Button below last assistant message */}
            {!isUser && isLast && onRegenerate && (
              <div className="mt-3 flex justify-start">
                <button
                  onClick={() => onRegenerate(index)}
                  className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-[10px] font-bold cursor-pointer border-none glass glass-hover transition"
                  style={{ color: "var(--text-secondary)" }}
                >
                  <RotateCw size={10} />
                  {t.regenerate}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
