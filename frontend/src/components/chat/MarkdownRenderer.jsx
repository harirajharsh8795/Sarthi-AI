import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function MarkdownRenderer({ content }) {
  if (!content) return null;

  return (
    <div className="markdown-prose w-full text-[16px] leading-[1.7] font-normal" style={{ color: "var(--text-primary)" }}>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({node, ...props}) => <h1 className="text-2xl font-extrabold mt-6 mb-3" style={{ color: "var(--text-primary)" }} {...props} />,
          h2: ({node, ...props}) => <h2 className="text-xl font-bold mt-5 mb-2.5" style={{ color: "var(--text-primary)" }} {...props} />,
          h3: ({node, ...props}) => <h3 className="text-lg font-bold mt-4 mb-2" style={{ color: "var(--text-primary)" }} {...props} />,
          p: ({node, ...props}) => <p className="mb-3 leading-[1.7] text-[16px]" style={{ color: "var(--text-primary)" }} {...props} />,
          ul: ({node, ...props}) => <ul className="ml-5 list-disc pl-1 mb-3 space-y-2 text-[16px]" style={{ color: "var(--text-primary)" }} {...props} />,
          ol: ({node, ...props}) => <ol className="ml-6 list-decimal pl-1 mb-3 space-y-2 text-[16px]" style={{ color: "var(--text-primary)" }} {...props} />,
          li: ({node, ...props}) => <li className="leading-[1.7]" style={{ color: "var(--text-primary)" }} {...props} />,
          strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
          em: ({node, ...props}) => <em className="italic" {...props} />,
          blockquote: ({node, ...props}) => (
            <blockquote 
              className="border-l-4 pl-4 py-1.5 my-3 opacity-95 italic text-[15.5px]" 
              style={{ borderColor: "var(--accent)" }} 
              {...props} 
            />
          ),
          table: ({node, ...props}) => (
            <div className="overflow-x-auto mb-4 border rounded-xl" style={{ borderColor: "var(--border)" }}>
              <table className="w-full text-left border-collapse text-[15px]" {...props} />
            </div>
          ),
          th: ({node, ...props}) => (
            <th className="p-3 border-b font-bold bg-white/5 text-[15px]" style={{ borderColor: "var(--border)", color: "var(--text-primary)" }} {...props} />
          ),
          td: ({node, ...props}) => (
            <td className="p-3 border-b text-[15px]" style={{ borderColor: "var(--border)" }} {...props} />
          ),
          code: ({node, inline, ...props}) => 
            inline ? (
              <code className="px-2 py-0.5 rounded text-[14px] font-mono bg-white/10" style={{ color: "var(--text-primary)" }} {...props} />
            ) : (
              <pre className="p-4 my-3 rounded-xl overflow-x-auto text-[14px] font-mono bg-[#0A0718] border" style={{ borderColor: "var(--border)" }}>
                <code {...props} />
              </pre>
            ),
          hr: ({node, ...props}) => <hr className="my-5 border-t opacity-30" style={{ borderColor: "var(--border)" }} {...props} />,
          a: ({node, ...props}) => <a className="underline hover:opacity-80 transition-opacity font-medium" style={{ color: "var(--accent)" }} target="_blank" rel="noopener noreferrer" {...props} />
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
