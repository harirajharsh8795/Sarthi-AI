import React, { useState, useEffect } from "react";
import { Edit3, Check, X, FileText, Menu } from "lucide-react";
import { translations } from "../../utils/localization";

export default function ChatHeader({
  activeConversationId,
  conversations,
  onRenameConversation,
  documentsCount,
  language,
  onToggleMobileSidebar
}) {
  const t = translations[language] || translations.en;
  
  const currentConv = conversations.find((c) => c.id === activeConversationId);
  const currentTitle = currentConv ? currentConv.title : "Saarthi AI Chat";

  const [isEditing, setIsEditing] = useState(false);
  const [titleInput, setTitleInput] = useState(currentTitle);

  useEffect(() => {
    setTitleInput(currentTitle);
  }, [currentTitle]);

  const handleRename = () => {
    if (titleInput.trim() && titleInput !== currentTitle) {
      onRenameConversation(activeConversationId, titleInput.trim());
    }
    setIsEditing(false);
  };

  return (
    <header
      className="h-14 px-4 md:px-6 flex justify-between items-center flex-shrink-0 transition-colors duration-150 glass border-b z-10"
      style={{ borderColor: "var(--border)" }}
    >
      {/* Left: Hamburger menu (mobile) + Breadcrumbs / Editable Title */}
      <div className="flex items-center gap-2">
        <button
          onClick={onToggleMobileSidebar}
          className="md:hidden p-1.5 rounded-lg border hover:bg-white/10 text-white/80 cursor-pointer"
          style={{ borderColor: "var(--border)" }}
          title="Open Menu"
        >
          <Menu className="w-4 h-4" />
        </button>

        <span className="text-[10px] font-bold tracking-wider" style={{ color: "var(--text-muted)" }}>
          SAARTHI AI
        </span>
        <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>
          &gt;
        </span>
        
        {isEditing ? (
          <div className="flex items-center gap-1">
            <input
              type="text"
              value={titleInput}
              onChange={(e) => setTitleInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleRename()}
              className="px-2 py-0.5 text-xs rounded border bg-transparent focus:outline-none"
              style={{
                color: "var(--text-primary)",
                borderColor: "var(--accent)"
              }}
              autoFocus
            />
            <button
              onClick={handleRename}
              className="p-1 text-green-500 hover:bg-white/5 rounded cursor-pointer border-none bg-transparent"
            >
              <Check size={12} />
            </button>
            <button
              onClick={() => {
                setTitleInput(currentTitle);
                setIsEditing(false);
              }}
              className="p-1 text-red-500 hover:bg-white/5 rounded cursor-pointer border-none bg-transparent"
            >
              <X size={12} />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2 group/title">
            <h2 className="text-xs font-black select-none truncate max-w-[200px]" style={{ color: "var(--text-primary)" }}>
              {currentTitle}
            </h2>
            <button
              onClick={() => setIsEditing(true)}
              className="opacity-0 group-hover/title:opacity-100 p-0.5 rounded text-slate-400 hover:text-slate-200 cursor-pointer border-none bg-transparent transition-opacity"
              title={t.renameConversation}
            >
              <Edit3 size={10} />
            </button>
          </div>
        )}
      </div>

      {/* Right: Document count badge */}
      {documentsCount > 0 && (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[10px] font-bold" style={{ borderColor: "var(--border)" }}>
          <FileText size={10} className="text-purple-500 animate-pulse" />
          <span style={{ color: "var(--text-secondary)" }}>
            {documentsCount} {documentsCount === 1 ? "doc" : "docs"}
          </span>
        </div>
      )}
    </header>
  );
}
