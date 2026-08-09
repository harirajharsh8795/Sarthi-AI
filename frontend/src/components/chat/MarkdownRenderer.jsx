import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  return (
    <div className="markdown-prose w-full text-[14.5px] leading-[1.65] font-normal" style={{ color: "var(--text-primary)" }}>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({node, ...props}) => <h1 className="text-xl font-extrabold mt-5 mb-2.5" style={{ color: "var(--text-primary)" }} {...props} />,
          h2: ({node, ...props}) => <h2 className="text-lg font-bold mt-4 mb-2" style={{ color: "var(--text-primary)" }} {...props} />,
          h3: ({node, ...props}) => <h3 className="text-[15.5px] font-bold mt-3.5 mb-2" style={{ color: "var(--text-primary)" }} {...props} />,
          p: ({node, ...props}) => <p className="mb-2.5 leading-relaxed text-[14.5px]" style={{ color: "var(--text-primary)" }} {...props} />,
          ul: ({node, ...props}) => <ul className="ml-4 list-disc pl-1 mb-2.5 space-y-1.5 text-[14.5px]" style={{ color: "var(--text-primary)" }} {...props} />,
          ol: ({node, ...props}) => <ol className="ml-5 list-decimal pl-1 mb-2.5 space-y-1.5 text-[14.5px]" style={{ color: "var(--text-primary)" }} {...props} />,
          li: ({node, ...props}) => <li className="leading-relaxed" style={{ color: "var(--text-primary)" }} {...props} />,
          strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
          em: ({node, ...props}) => <em className="italic" {...props} />,
          blockquote: ({node, ...props}) => (
            <blockquote 
              className="border-l-2 pl-3 py-1 my-2.5 opacity-90 italic text-[14px]" 
              style={{ borderColor: "var(--accent)" }} 
              {...props} 
            />
          ),
          table: ({node, ...props}) => (
            <div className="overflow-x-auto mb-3 border rounded-lg" style={{ borderColor: "var(--border)" }}>
              <table className="w-full text-left border-collapse text-[13.5px]" {...props} />
            </div>
          ),
          th: ({node, ...props}) => (
            <th className="p-2.5 border-b font-bold bg-white/5" style={{ borderColor: "var(--border)", color: "var(--text-primary)" }} {...props} />
          ),
          td: ({node, ...props}) => (
            <td className="p-2.5 border-b" style={{ borderColor: "var(--border)" }} {...props} />
          ),
          code: ({node, inline, ...props}) => 
            inline ? (
              <code className="px-1.5 py-0.5 rounded text-[12.5px] font-mono bg-white/10" style={{ color: "var(--text-primary)" }} {...props} />
            ) : (
              <pre className="p-3 my-2.5 rounded-xl overflow-x-auto text-[12.5px] font-mono bg-[#0A0718] border" style={{ borderColor: "var(--border)" }}>
                <code {...props} />
              </pre>
            ),
          hr: ({node, ...props}) => <hr className="my-4 border-t opacity-30" style={{ borderColor: "var(--border)" }} {...props} />,
          a: ({node, ...props}) => <a className="underline hover:opacity-80 transition-opacity font-medium" style={{ color: "var(--accent)" }} target="_blank" rel="noopener noreferrer" {...props} />
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
