import { motion } from "framer-motion";
import { Brain } from "lucide-react";
import MarkdownRenderer from "./MarkdownRenderer";

/**
 * Animated typing indicator shown during LLM streaming.
 * Shows bouncing dots when waiting, or streaming text with cursor.
 */
export default function TypingIndicator({ streamText, streamCitations, onCitationClick, language }) {
  // Streaming text mode
  if (streamText) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex w-full justify-start mb-4"
      >
        {/* Avatar */}
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mr-3 shadow-lg select-none"
          style={{ background: "var(--accent-gradient)", color: "white" }}
        >
          <Brain className="w-4 h-4 text-white" />
        </div>

        <div className="flex-1 text-left text-sm leading-relaxed max-w-[calc(100%-44px)]" style={{ color: "var(--text-primary)" }}>
          <MarkdownRenderer content={streamText} />
          {/* Blinking cursor */}
          <span
            className="inline-block w-0.5 h-4 ml-0.5 align-middle mt-1"
            style={{
              background: "var(--accent)",
              animation: "pulse 1s ease-in-out infinite",
            }}
          />

          {/* Stream citations */}
          {streamCitations && streamCitations.length > 0 && (
            <div className="mt-4 pt-3" style={{ borderTop: "1px solid var(--border)" }}>
              <p
                className="text-[9px] font-bold uppercase tracking-wider mb-2"
                style={{ color: "var(--text-muted)" }}
              >
                {language === "hi" ? "स्रोत" : "Sources"}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {streamCitations.map((cit) => (
                  <button
                    key={cit.index}
                    onClick={() => onCitationClick?.(cit)}
                    className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium cursor-pointer border-none glass glass-hover transition"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    <span
                      className="text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold"
                      style={{
                        background: "var(--accent-muted)",
                        color: "var(--accent)",
                        border: "1px solid rgba(139,92,246,0.3)",
                      }}
                    >
                      {cit.index}
                    </span>
                    <span className="truncate max-w-[120px]">{cit.filename}</span>
                    <span className="text-[9px]" style={{ color: "var(--text-muted)" }}>
                      {language === "hi" ? "पृष्ठ" : "P"}{cit.page_number}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </motion.div>
    );
  }

  // Bouncing dots mode (waiting for first token)
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex w-full justify-start mb-4"
    >
      {/* Avatar */}
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mr-3 shadow-lg select-none"
        style={{ background: "var(--accent-gradient)", color: "white" }}
      >
        <Brain className="w-4 h-4 text-white" />
      </div>

      <div
        className="flex items-center space-x-1.5 px-4 py-2.5 rounded-2xl glass"
      >
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: "var(--accent)" }}
            animate={{
              scale: [1, 1.4, 1],
              opacity: [0.4, 1, 0.4],
            }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              delay: i * 0.15,
            }}
          />
        ))}
      </div>
    </motion.div>
  );
}
