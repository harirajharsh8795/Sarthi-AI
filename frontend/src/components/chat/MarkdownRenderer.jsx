import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  return (
    <div className="markdown-prose w-full text-xs leading-relaxed" style={{ color: "var(--text-secondary)" }}>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({node, ...props}) => <h1 className="text-lg font-bold mt-4 mb-2" style={{ color: "var(--text-primary)" }} {...props} />,
          h2: ({node, ...props}) => <h2 className="text-base font-bold mt-4 mb-2" style={{ color: "var(--text-primary)" }} {...props} />,
          h3: ({node, ...props}) => <h3 className="text-sm font-bold mt-3 mb-1.5" style={{ color: "var(--text-primary)" }} {...props} />,
          p: ({node, ...props}) => <p className="mb-2" {...props} />,
          ul: ({node, ...props}) => <ul className="ml-4 list-disc pl-1 mb-2 space-y-1" {...props} />,
          ol: ({node, ...props}) => <ol className="ml-5 list-decimal pl-1 mb-2 space-y-1" {...props} />,
          li: ({node, ...props}) => <li {...props} />,
          strong: ({node, ...props}) => <strong className="font-bold" style={{ color: "var(--text-primary)" }} {...props} />,
          em: ({node, ...props}) => <em className="italic" {...props} />,
          blockquote: ({node, ...props}) => (
            <blockquote 
              className="border-l-2 pl-3 py-0.5 my-2 opacity-80 italic" 
              style={{ borderColor: "var(--accent)" }} 
              {...props} 
            />
          ),
          table: ({node, ...props}) => (
            <div className="overflow-x-auto mb-3 border rounded-lg" style={{ borderColor: "var(--border)" }}>
              <table className="w-full text-left border-collapse text-xs" {...props} />
            </div>
          ),
          th: ({node, ...props}) => (
            <th className="p-2 border-b font-bold bg-white/5" style={{ borderColor: "var(--border)", color: "var(--text-primary)" }} {...props} />
          ),
          td: ({node, ...props}) => (
            <td className="p-2 border-b" style={{ borderColor: "var(--border)" }} {...props} />
          ),
          code: ({node, inline, ...props}) => 
            inline ? (
              <code className="px-1.5 py-0.5 rounded text-[11px] font-mono bg-white/10" style={{ color: "var(--text-primary)" }} {...props} />
            ) : (
              <pre className="p-3 my-2 rounded-xl overflow-x-auto text-[11px] font-mono bg-[#0A0718] border" style={{ borderColor: "var(--border)" }}>
                <code {...props} />
              </pre>
            ),
          hr: ({node, ...props}) => <hr className="my-4 border-t opacity-30" style={{ borderColor: "var(--border)" }} {...props} />,
          a: ({node, ...props}) => <a className="underline hover:opacity-80 transition-opacity" style={{ color: "var(--accent)" }} target="_blank" rel="noopener noreferrer" {...props} />
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
