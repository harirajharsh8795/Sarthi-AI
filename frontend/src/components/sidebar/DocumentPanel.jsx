import React, { useState, useEffect } from "react";
import { 
  FileText, Image as ImageIcon, Trash2, RefreshCw, ChevronDown, ChevronUp, AlertCircle 
} from "lucide-react";
import { translations } from "../../utils/localization";

const API_BASE = "http://localhost:8000";

export default function DocumentPanel({ sessionId, conversationId, refreshTrigger, language }) {
  const t = translations[language] || translations.en;
  
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [deletingDocId, setDeletingDocId] = useState(null);
  const [deletingLoading, setDeletingLoading] = useState(false);

  // Group collapses states
  const [collapsedGroups, setCollapsedGroups] = useState({
    pdf: false,
    docx: false,
    images: false
  });

  const fetchHistory = async () => {
    if (!sessionId) return;
    setLoading(true);
    setError(null);
    try {
      const url = `${API_BASE}/api/history?session_id=${sessionId}${
        conversationId ? `&conversation_id=${conversationId}` : ""
      }`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Failed to load documents");
      }
      const data = await response.json();
      setDocuments(data.documents || []);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
    setDeletingDocId(null);
  }, [sessionId, conversationId, refreshTrigger]);

  const handleDeleteClick = (e, docId) => {
    e.stopPropagation();
    setDeletingDocId(docId);
  };

  const handleCancelDelete = (e) => {
    e.stopPropagation();
    setDeletingDocId(null);
  };

  const handleConfirmDelete = async (e, docId) => {
    e.stopPropagation();
    setDeletingLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/document/${docId}?session_id=${sessionId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete document");
      }

      setDeletingDocId(null);
      fetchHistory();
    } catch (err) {
      console.error("Deletion failed:", err);
      alert("Error deleting: " + err.message);
    } finally {
      setDeletingLoading(false);
    }
  };

  const getFileIcon = (fileType) => {
    const ext = (fileType || "").toLowerCase();
    if (ext === ".pdf") return <FileText size={14} className="text-red-500 flex-shrink-0" />;
    if (ext === ".docx") return <FileText size={14} className="text-blue-500 flex-shrink-0" />;
    return <ImageIcon size={14} className="text-green-500 flex-shrink-0" />;
  };

  // Group by document type helper
  const groupDocs = () => {
    const pdfs = [];
    const docxFiles = [];
    const images = [];

    documents.forEach((d) => {
      const ext = (d.file_type || "").toLowerCase();
      if (ext === ".pdf") pdfs.push(d);
      else if (ext === ".docx") docxFiles.push(d);
      else images.push(d);
    });

    return { pdfs, docxFiles, images };
  };

  const { pdfs, docxFiles, images } = groupDocs();

  const toggleGroup = (groupKey) => {
    setCollapsedGroups((prev) => ({
      ...prev,
      [groupKey]: !prev[groupKey]
    }));
  };

  const formatTimestamp = (ts) => {
    if (!ts) return "";
    try {
      const date = new Date(ts.replace(" ", "T"));
      return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
    } catch {
      return ts;
    }
  };

  const renderDocRow = (doc) => {
    const isDeleting = deletingDocId === doc.document_id;
    if (isDeleting) {
      return (
        <div key={doc.document_id} className="p-2 border rounded-xl bg-red-950/20 text-left space-y-1.5" style={{ borderColor: "var(--danger)" }}>
          <p className="text-[9px] font-semibold text-red-400">
            {t.confirmDelete.replace("document", doc.original_filename)}
          </p>
          <div className="flex items-center gap-1.5">
            <button
              onClick={(e) => handleConfirmDelete(e, doc.document_id)}
              disabled={deletingLoading}
              className="px-2 py-0.5 bg-red-600 hover:bg-red-500 text-white rounded text-[9px] font-bold cursor-pointer disabled:opacity-50 border-none"
            >
              {t.confirm}
            </button>
            <button
              onClick={handleCancelDelete}
              disabled={deletingLoading}
              className="px-2 py-0.5 bg-white/5 hover:bg-white/10 text-slate-300 rounded text-[9px] font-bold cursor-pointer border-none"
            >
              {t.cancel}
            </button>
          </div>
        </div>
      );
    }

    return (
      <div
        key={doc.document_id}
        className="group/doc flex items-center justify-between p-2 rounded-xl border hover:bg-[var(--surface-hover)] transition relative text-left"
        style={{ borderColor: "var(--border)", background: "var(--bg-primary)" }}
      >
        <div className="flex items-center gap-2 truncate pr-8">
          {getFileIcon(doc.file_type)}
          <div className="truncate">
            <p className="text-[10px] font-bold truncate" style={{ color: "var(--text-primary)" }} title={doc.original_filename}>
              {doc.original_filename}
            </p>
            <p className="text-[8px] font-medium" style={{ color: "var(--text-secondary)" }}>
              {doc.page_count ? `${doc.page_count}p` : ""} 
              {doc.chunk_count ? ` • ${doc.chunk_count} chunks` : ""}
              {doc.uploaded_at ? ` • ${formatTimestamp(doc.uploaded_at)}` : ""}
            </p>
          </div>
        </div>

        {/* Index Status Badge */}
        <div className="absolute right-2 top-2 group-hover/doc:opacity-0 transition-opacity">
          <span className={`badge text-[8px] px-1 py-0.5 ${
            doc.status === "indexed" 
              ? "badge-success" 
              : doc.status === "failed" 
              ? "badge-danger" 
              : "badge-warning"
          }`}>
            {doc.status === "indexed" 
              ? t.statusIndexed 
              : doc.status === "failed" 
              ? t.statusFailed 
              : t.statusPending}
          </span>
        </div>

        {/* Hover Delete Action */}
        <button
          type="button"
          onClick={(e) => handleDeleteClick(e, doc.document_id)}
          className="opacity-0 group-hover/doc:opacity-100 transition absolute right-2 top-2 p-0.5 text-slate-400 hover:text-red-400 bg-transparent border-none cursor-pointer"
          title="Delete document"
        >
          <Trash2 size={12} />
        </button>
      </div>
    );
  };

  return (
    <div className="flex flex-col space-y-3.5">
      {loading && documents.length === 0 ? (
        <div className="flex justify-center items-center py-4">
          <svg className="animate-spin h-4 w-4 text-purple-500" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>
      ) : error ? (
        <p className="text-red-400 text-[10px] text-center">{error}</p>
      ) : documents.length === 0 ? (
        <div className="text-center py-4 text-slate-500 text-[10px] leading-relaxed">
          {t.noDocs}
        </div>
      ) : (
        <div className="space-y-3 overflow-y-auto max-h-[160px] custom-scrollbar pr-0.5">
          {/* PDF Group */}
          {pdfs.length > 0 && (
            <div className="space-y-1">
              <button
                onClick={() => toggleGroup("pdf")}
                className="w-full flex justify-between items-center text-[9px] font-bold text-slate-500 uppercase tracking-wider py-1 border-none bg-transparent cursor-pointer"
              >
                <span>📄 PDF ({pdfs.length})</span>
                {collapsedGroups.pdf ? <ChevronDown size={10} /> : <ChevronUp size={10} />}
              </button>
              {!collapsedGroups.pdf && (
                <div className="space-y-1 pl-1">{pdfs.map(renderDocRow)}</div>
              )}
            </div>
          )}

          {/* DOCX Group */}
          {docxFiles.length > 0 && (
            <div className="space-y-1">
              <button
                onClick={() => toggleGroup("docx")}
                className="w-full flex justify-between items-center text-[9px] font-bold text-slate-500 uppercase tracking-wider py-1 border-none bg-transparent cursor-pointer"
              >
                <span>📝 DOCX ({docxFiles.length})</span>
                {collapsedGroups.docx ? <ChevronDown size={10} /> : <ChevronUp size={10} />}
              </button>
              {!collapsedGroups.docx && (
                <div className="space-y-1 pl-1">{docxFiles.map(renderDocRow)}</div>
              )}
            </div>
          )}

          {/* Images Group */}
          {images.length > 0 && (
            <div className="space-y-1">
              <button
                onClick={() => toggleGroup("images")}
                className="w-full flex justify-between items-center text-[9px] font-bold text-slate-500 uppercase tracking-wider py-1 border-none bg-transparent cursor-pointer"
              >
                <span>🖼 Images ({images.length})</span>
                {collapsedGroups.images ? <ChevronDown size={10} /> : <ChevronUp size={10} />}
              </button>
              {!collapsedGroups.images && (
                <div className="space-y-1 pl-1">{images.map(renderDocRow)}</div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
