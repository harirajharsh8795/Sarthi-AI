import React, { useState } from "react";
import { Trash2, Edit3, Check, X, MessageSquare } from "lucide-react";
import { translations } from "../utils/localization";

export default function ConversationList({
  conversations,
  activeConversationId,
  onConversationClick,
  onDeleteConversation,
  onRenameConversation,
  language
}) {
  const t = translations[language] || translations.en;
  
  const [editingId, setEditingId] = useState(null);
  const [renameInput, setRenameInput] = useState("");

  const handleStartRename = (e, c) => {
    e.stopPropagation();
    setEditingId(c.id);
    setRenameInput(c.title || "");
  };

  const handleSaveRename = (e, id) => {
    e.stopPropagation();
    if (renameInput.trim()) {
      onRenameConversation(id, renameInput.trim());
    }
    setEditingId(null);
  };

  const handleCancelRename = (e) => {
    e.stopPropagation();
    setEditingId(null);
  };

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (confirm(t.confirmDeleteConversation || "Delete this conversation?")) {
      onDeleteConversation(id);
    }
  };

  const groupConversationsByDate = (convs) => {
    const groups = {
      [t.today]: [],
      [t.yesterday]: [],
      [t.thisWeek]: [],
      [t.older]: []
    };
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const startOfWeek = new Date(today);
    startOfWeek.setDate(startOfWeek.getDate() - today.getDay());

    convs.forEach((c) => {
      if (!c.updated_at) {
        groups[t.older].push(c);
        return;
      }
      
      const date = new Date(c.updated_at.replace(" ", "T"));
      date.setHours(0, 0, 0, 0);

      const diffTime = today - date;
      const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) {
        groups[t.today].push(c);
      } else if (diffDays === 1) {
        groups[t.yesterday].push(c);
      } else if (diffDays <= 7) {
        groups[t.thisWeek].push(c);
      } else {
        groups[t.older].push(c);
      }
    });

    return groups;
  };

  const grouped = groupConversationsByDate(conversations);

  return (
    <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5 custom-scrollbar">
      {Object.entries(grouped).map(([groupName, groupItems]) => {
        if (groupItems.length === 0) return null;
        return (
          <div key={groupName} className="space-y-1">
            <h4 className="px-2.5 text-[9px] font-bold text-slate-500 uppercase tracking-wider">
              {groupName}
            </h4>
            <div className="space-y-0.5">
              {groupItems.map((c) => {
                const isActive = c.id === activeConversationId;
                const isEditing = c.id === editingId;

                if (isEditing) {
                  return (
                    <div 
                      key={c.id} 
                      className="w-full flex items-center gap-1 px-2.5 py-1.5 rounded-lg border glass bg-white/5"
                      style={{ borderColor: "var(--accent)" }}
                    >
                      <input
                        type="text"
                        value={renameInput}
                        onChange={(e) => setRenameInput(e.target.value)}
                        className="bg-transparent border-none text-[11px] focus:outline-none flex-1"
                        style={{ color: "var(--text-primary)" }}
                        autoFocus
                      />
                      <button
                        onClick={(e) => handleSaveRename(e, c.id)}
                        className="p-0.5 text-green-500 hover:bg-white/5 rounded cursor-pointer border-none bg-transparent"
                      >
                        <Check size={11} />
                      </button>
                      <button
                        onClick={handleCancelRename}
                        className="p-0.5 text-red-500 hover:bg-white/5 rounded cursor-pointer border-none bg-transparent"
                      >
                        <X size={11} />
                      </button>
                    </div>
                  );
                }

                return (
                  <button
                    key={c.id}
                    onClick={() => onConversationClick(c.id)}
                    className={`sidebar-chat-item group/item text-left px-2.5 py-2 rounded-lg text-[11px] transition truncate cursor-pointer flex items-center justify-between border ${
                      isActive ? "active" : ""
                    }`}
                    title={c.title}
                  >
                    <div className="flex items-center gap-2 truncate flex-1">
                      <MessageSquare size={12} className="flex-shrink-0" />
                      <span className="truncate">{c.title || "New Conversation"}</span>
                    </div>

                    {/* Actions popup on hover */}
                    <div className="opacity-0 group-hover/item:opacity-100 flex items-center gap-1 transition-opacity">
                      <button
                        onClick={(e) => handleStartRename(e, c)}
                        className="p-0.5 hover:bg-[var(--surface-hover)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] rounded cursor-pointer border-none bg-transparent"
                        title={t.renameConversation}
                      >
                        <Edit3 size={11} />
                      </button>
                      <button
                        onClick={(e) => handleDelete(e, c.id)}
                        className="p-0.5 hover:bg-[var(--surface-hover)] text-[var(--text-secondary)] hover:text-red-500 rounded cursor-pointer border-none bg-transparent"
                        title={t.deleteConversation}
                      >
                        <Trash2 size={11} />
                      </button>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

