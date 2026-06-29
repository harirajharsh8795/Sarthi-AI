import React from "react";
import { motion } from "framer-motion";
import { translations } from "../../utils/localization";
import { Check, AlertCircle } from "lucide-react";

export default function UploadTimeline({ step, error, language }) {
  const t = translations[language] || translations.en;

  const steps = [
    { key: "uploading", label: t.uploadTimeline_uploading || "Uploading..." },
    { key: "ocr", label: t.uploadTimeline_ocr || "OCR Processing..." },
    { key: "embedding", label: t.uploadTimeline_embedding || "Embedding..." },
    { key: "indexing", label: t.uploadTimeline_indexing || "Indexing..." },
    { key: "ready", label: t.uploadTimeline_ready || "Ready" }
  ];

  const getStepStatus = (index) => {
    if (error && index === step) return "failed";
    if (step > index) return "complete";
    if (step === index) return "active";
    return "inactive";
  };

  return (
    <div className="w-full py-3 px-4 glass rounded-xl flex flex-col space-y-2 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-purple-500 animate-pulse" />
          <span className="text-xs font-semibold" style={{ color: "var(--text-primary)" }}>
            {error ? (language === "hi" ? "दस्तावेज़ विफलता" : "Ingestion Failed") : (language === "hi" ? "दस्तावेज़ प्रसंस्करण" : "Processing Document")}
          </span>
        </div>
        {error && (
          <span className="text-[10px] font-medium text-red-500 flex items-center gap-1">
            <AlertCircle size={10} />
            {error}
          </span>
        )}
      </div>

      <div className="flex items-center justify-between relative pt-2">
        {/* Connection line */}
        <div className="absolute top-5 left-4 right-4 h-0.5 bg-white/5 -z-10">
          <motion.div 
            className="h-full" 
            style={{ background: "var(--accent)" }}
            initial={{ width: "0%" }}
            animate={{ width: `${(step / (steps.length - 1)) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>

        {steps.map((s, idx) => {
          const status = getStepStatus(idx);
          
          return (
            <div key={s.key} className="flex flex-col items-center space-y-1.5 flex-1 relative">
              <div 
                className={`w-6 h-6 rounded-full flex items-center justify-center border text-[10px] font-bold transition-all duration-300 ${
                  status === "complete"
                    ? "bg-purple-600 border-purple-500 text-white shadow-md"
                    : status === "active"
                    ? "bg-[#0A0718] border-purple-500 text-purple-400 shadow-md animate-pulse-glow"
                    : status === "failed"
                    ? "bg-red-950 border-red-500 text-red-400"
                    : "bg-[#0A0718] border-white/10 text-slate-500"
                }`}
              >
                {status === "complete" ? (
                  <Check size={12} strokeWidth={3} />
                ) : status === "failed" ? (
                  <AlertCircle size={12} />
                ) : (
                  idx + 1
                )}
              </div>
              <span 
                className={`text-[8px] font-bold text-center select-none ${
                  status === "active" ? "text-purple-400" : "text-slate-500"
                }`}
              >
                {s.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
