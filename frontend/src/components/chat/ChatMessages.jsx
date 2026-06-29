import React from "react";
import MessageBubble from "./MessageBubble";
import EmptyState from "./EmptyState";

export default function ChatMessages({
  messages,
  onCitationClick,
  onSuggestionClick,
  recentDocs,
  language,
  onDeleteMessage,
  onEditMessage,
  onRegenerateMessage,
  messagesEndRef
}) {
  const isChatEmpty =
    messages.length === 0 ||
    (messages.length === 1 &&
      messages[0].role === "assistant" &&
      (messages[0].content.startsWith("Hello! I am Saarthi") ||
        messages[0].content.startsWith("नमस्ते! मैं सारथी")));

  return (
    <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 custom-scrollbar">
      {isChatEmpty ? (
        <EmptyState
          language={language}
          onSuggestionClick={onSuggestionClick}
          recentDocs={recentDocs}
        />
      ) : (
        <div className="max-w-2xl mx-auto space-y-6">
          {messages.map((msg, idx) => (
            <MessageBubble
              key={msg.id || idx}
              index={idx}
              message={msg}
              onCitationClick={onCitationClick}
              language={language}
              onDelete={onDeleteMessage}
              onEdit={onEditMessage}
              onRegenerate={onRegenerateMessage}
              isLast={idx === messages.length - 1}
            />
          ))}
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}
