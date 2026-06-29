import React, { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Camera, Image } from "lucide-react";
import { translations } from "../../utils/localization";

export default function AttachmentMenu({ isOpen, onClose, onOptionClick, language }) {
  const t = translations[language] || translations.en;
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const options = [
    {
      key: "document",
      label: t.uploadDoc,
      icon: FileText,
      iconColor: "text-purple-500",
    },
    {
      key: "camera",
      label: t.takePhoto,
      icon: Camera,
      iconColor: "text-green-500",
    },
    {
      key: "photo",
      label: t.uploadPhoto,
      icon: Image,
      iconColor: "text-emerald-500",
    },
  ];

  return (
    <AnimatePresence>
      <motion.div
        ref={menuRef}
        initial={{ opacity: 0, y: 8, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 8, scale: 0.95 }}
        transition={{ duration: 0.15 }}
        className="absolute bottom-12 left-0 w-56 rounded-xl shadow-xl py-1.5 z-20 text-left glass-strong"
      >
        {options.map((opt) => {
          const Icon = opt.icon;
          return (
            <button
              key={opt.key}
              type="button"
              onClick={() => {
                onOptionClick(opt.key);
                onClose();
              }}
              className="w-full px-4 py-2.5 hover:bg-white/5 text-xs font-semibold flex items-center space-x-3 border-none bg-transparent cursor-pointer transition-colors"
              style={{ color: "var(--text-secondary)" }}
            >
              <Icon size={16} className={opt.iconColor} />
              <span style={{ color: "var(--text-primary)" }}>{opt.label}</span>
            </button>
          );
        })}
      </motion.div>
    </AnimatePresence>
  );
}
