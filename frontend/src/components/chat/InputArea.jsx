import React, { useState, useRef, useEffect } from "react";
import { Plus, Mic, Send, Square, X, AlertCircle } from "lucide-react";
import AttachmentMenu from "./AttachmentMenu";
import { translations } from "../../utils/localization";

export default function InputArea({
  input,
  setInput,
  isStreaming,
  transcribing,
  isRecording,
  uploadingFile,
  attachedFile,
  setAttachedFile,
  inlineError,
  setInlineError,
  onSend,
  onStopStreaming,
  toggleRecording,
  triggerDocUpload,
  triggerPhotoUpload,
  triggerCameraOpen,
  documentsList, // list of documents to support @mentions
  onDeleteDocument,
  language
}) {
  const t = translations[language] || translations.en;
  const textareaRef = useRef(null);
  const [attachmentMenuOpen, setAttachmentMenuOpen] = useState(false);
  const [showMentionDropdown, setShowMentionDropdown] = useState(false);
  const [mentionQuery, setMentionQuery] = useState("");
  const dropdownRef = useRef(null);

  // Resize textarea on input change
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  // Handle @mentions detection
  useEffect(() => {
    const atIndex = input.lastIndexOf("@");
    if (atIndex !== -1 && (atIndex === 0 || input[atIndex - 1] === " ")) {
      const query = input.slice(atIndex + 1);
      // Ensure there are no spaces in the query to continue listing
      if (!query.includes(" ")) {
        setMentionQuery(query.toLowerCase());
        setShowMentionDropdown(true);
        return;
      }
    }
    setShowMentionDropdown(false);
  }, [input]);

  // Handle click outside mention dropdown
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setShowMentionDropdown(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handlePaste = (e) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") !== -1) {
        const file = items[i].getAsFile();
        if (file) {
          e.preventDefault();
          // Ensure it satisfies limit (15MB)
          if (file.size > 15 * 1024 * 1024) {
            setInlineError("File exceeds maximum size limit of 15MB.");
            return;
          }
          setAttachedFile(file);
          setInlineError(null);
        }
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (transcribing || isRecording || uploadingFile) return;
    if (!input.trim() && !attachedFile) return;
    if (isStreaming) {
      onStopStreaming();
      setTimeout(() => {
        onSend();
      }, 50);
    } else {
      onSend();
    }
  };

  const selectMention = (docName) => {
    const atIndex = input.lastIndexOf("@");
    if (atIndex !== -1) {
      const prefix = input.substring(0, atIndex);
      setInput(prefix + `@${docName} `);
    }
    setShowMentionDropdown(false);
    textareaRef.current?.focus();
  };

  const filteredDocs = documentsList
    ? documentsList.filter((doc) =>
        doc.original_filename.toLowerCase().includes(mentionQuery)
      )
    : [];

  return (
    <div className="relative w-full max-w-2xl mx-auto flex flex-col space-y-2 animate-slide-up">
      {/* Documents are now rendered in the ChatWorkspace messages flow instead of here */}

      {/* Mention Dropdown */}
      {showMentionDropdown && filteredDocs.length > 0 && (
        <div
          ref={dropdownRef}
          className="absolute bottom-16 left-2 w-64 glass-strong rounded-xl shadow-xl max-h-48 overflow-y-auto z-30 py-1 text-left border"
          style={{ borderColor: "var(--border)" }}
        >
          {filteredDocs.map((doc) => (
            <button
              key={doc.document_id}
              onClick={() => selectMention(doc.original_filename)}
              className="w-full px-3 py-2 text-xs font-medium cursor-pointer border-none text-left flex items-center gap-2 hover:bg-white/5 transition"
              style={{ color: "var(--text-primary)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
              <span className="truncate">{doc.original_filename}</span>
            </button>
          ))}
        </div>
      )}

      {/* Input Form Box */}
      <form
        onSubmit={handleSubmit}
        className="flex flex-col bg-white/5 border rounded-2xl p-2 focus-within:ring-2 focus-within:ring-purple-500/20 focus-within:border-purple-500/80 transition duration-150 relative"
        style={{ borderColor: "var(--border)" }}
      >
        {/* Attached File Chip */}
        {attachedFile && (
          <div className="flex items-center gap-2 px-2 pb-2">
            <span className="text-purple-400 text-sm">📎</span>
            <span className="text-sm text-slate-300 truncate max-w-xs">{attachedFile.name}</span>
            {uploadingFile ? (
              <span className="text-xs text-purple-400 animate-pulse">Uploading...</span>
            ) : (
              <button onClick={() => setAttachedFile(null)} className="text-slate-500 hover:text-red-400 ml-auto bg-transparent border-none cursor-pointer">✕</button>
            )}
          </div>
        )}
        <div className="flex items-center space-x-2">
        {/* Attachment menu trigger */}
        <div className="relative">
          <button
            type="button"
            onClick={() => setAttachmentMenuOpen(!attachmentMenuOpen)}
            disabled={transcribing || isRecording}
            className="p-2 rounded-xl hover:bg-white/5 transition text-slate-400 hover:text-slate-200 cursor-pointer border-none bg-transparent disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            title={t.addAttachment}
          >
            <Plus size={18} />
          </button>
          <AttachmentMenu
            isOpen={attachmentMenuOpen}
            onClose={() => setAttachmentMenuOpen(false)}
            onOptionClick={(opt) => {
              if (opt === "document") triggerDocUpload();
              if (opt === "photo") triggerPhotoUpload();
              if (opt === "camera") triggerCameraOpen();
            }}
            language={language}
          />
        </div>

        {/* Custom expandable input */}
        <textarea
          ref={textareaRef}
          rows="1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onPaste={handlePaste}
          disabled={transcribing || isRecording}
          placeholder={
            transcribing
              ? t.transcribing
              : isRecording
              ? t.listening
              : t.inputPlaceholder
          }
          className="flex-1 px-2.5 py-1.5 bg-transparent border-none focus:outline-none text-xs text-slate-100 disabled:cursor-not-allowed resize-none max-h-[120px] custom-scrollbar overflow-y-auto leading-relaxed"
          style={{ color: "var(--text-primary)" }}
        />

        {/* Speech input button */}
        <button
          type="button"
          onClick={toggleRecording}
          disabled={transcribing}
          className={`p-2 rounded-xl transition duration-150 flex items-center justify-center cursor-pointer border-none ${
            isRecording
              ? "bg-red-500 text-white animate-pulse"
              : "bg-transparent text-slate-400 hover:bg-white/5 hover:text-slate-200"
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          title={isRecording ? t.stopRecord : t.recordVoice}
        >
          {transcribing ? (
            <svg className="animate-spin h-4 w-4 text-purple-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            <Mic size={16} />
          )}
        </button>

        {/* Send / Stop streaming button */}
        {isStreaming && !input.trim() ? (
          <button
            type="button"
            onClick={onStopStreaming}
            className="p-2.5 rounded-full text-white bg-red-500 hover:bg-red-600 flex items-center justify-center transition duration-150 border-none cursor-pointer shadow-md"
            title={t.stopBtn}
          >
            <Square size={14} className="fill-current" />
          </button>
        ) : (
          <button
            type="submit"
            disabled={transcribing || isRecording || uploadingFile || (!input.trim() && !attachedFile)}
            className={`p-2.5 rounded-full text-white flex items-center justify-center transition duration-150 border-none cursor-pointer ${
              transcribing || isRecording || uploadingFile || (!input.trim() && !attachedFile)
                ? "bg-white/5 text-slate-600 border border-white/5 cursor-not-allowed"
                : "bg-gradient-to-r from-purple-600 to-violet-500 hover:from-purple-500 hover:to-violet-400 shadow-md shadow-purple-600/25"
            }`}
          >
            <Send size={14} />
          </button>
        )}
        </div>
      </form>

      {/* Inline validation errors */}
      {inlineError && (
        <span className="text-[10px] text-red-500 font-semibold leading-none pl-1 self-start flex items-center gap-1">
          <AlertCircle size={10} />
          {inlineError}
        </span>
      )}
    </div>
  );
}
