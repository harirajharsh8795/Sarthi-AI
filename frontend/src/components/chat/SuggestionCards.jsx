import React from "react";
import { motion } from "framer-motion";
import { Scale, HeartPulse, Landmark } from "lucide-react";

export default function SuggestionCards({ language, onSuggestionClick }) {
  const cards = [
    {
      id: "medical",
      icon: HeartPulse,
      iconColor: "text-emerald-500",
      title: language === "hi" ? "चिकित्सा सहायता" : "Medical Assistant",
      desc: language === "hi" ? "उपचार दिशानिर्देश, लक्षण और दवाएं" : "Treatment guidelines, symptom checks, drug norms",
      query: language === "hi" ? "डेंगू बुखार के लक्षण और प्राथमिक उपचार क्या हैं?" : "Dengue fever symptoms and primary treatment guidelines?"
    },
    {
      id: "legal",
      icon: Scale,
      iconColor: "text-purple-500",
      title: language === "hi" ? "कानूनी सहायता" : "Legal Assistant",
      desc: language === "hi" ? "अधिकार, उपभोक्ता शिकायतें, RTI और FIR" : "Rights, consumer complaints, RTI, BNSS 2023",
      query: language === "hi" ? "RTI आवेदन लिखने की सही प्रक्रिया क्या है?" : "What is the procedure to file a Right to Information (RTI) application?"
    },
    {
      id: "banking",
      icon: Landmark,
      iconColor: "text-blue-500",
      title: language === "hi" ? "बैंकिंग सहायता" : "Banking Assistant",
      desc: language === "hi" ? "KYC नियम, ऋण और बैंक खाते की प्रक्रियाएं" : "KYC norms, loan queries, bank account operations",
      query: language === "hi" ? "RBI के नए नियमों के अनुसार बैंक में KYC कैसे अपडेट करें?" : "How to update KYC in bank per RBI guidelines?"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full">
      {cards.map((c) => {
        const Icon = c.icon;
        return (
          <motion.button
            key={c.id}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSuggestionClick(c.query)}
            className="card card-interactive p-4 text-left cursor-pointer border-none flex flex-col space-y-3 glass"
          >
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-white/5">
                <Icon size={18} className={c.iconColor} />
              </div>
              <h3 className="text-xs font-bold" style={{ color: "var(--text-primary)" }}>
                {c.title}
              </h3>
            </div>
            <p className="text-[10px] leading-relaxed flex-1" style={{ color: "var(--text-secondary)" }}>
              {c.desc}
            </p>
            <span className="text-[9px] font-semibold truncate hover:underline" style={{ color: "var(--accent)" }}>
              {language === "hi" ? "कोशिश करें →" : "Try asking →"}
            </span>
          </motion.button>
        );
      })}
    </div>
  );
}
