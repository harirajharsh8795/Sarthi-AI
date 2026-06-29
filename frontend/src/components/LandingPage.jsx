import React, { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence, useScroll, useTransform } from "framer-motion";
import { 
  Shield, Brain, HeartPulse, Scale, Landmark, FileText, CheckCircle2, 
  Server, Database, Sparkles, Cpu, Layers, Mic, Volume2, 
  Search, Eye, ArrowRight, Unlock, Network, Globe,
  Mail, MapPin, Phone, ChevronDown, ChevronUp
} from "lucide-react";

// Inline Github Icon to avoid package import mismatch
const GithubIcon = ({ className }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C19.138 20.197 22 16.44 22 12.017 22 6.484 17.522 2 12 2z" />
  </svg>
);

// Hook for counting animation
const useCounter = (end, duration = 2000, trigger = false) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!trigger) return;
    let startTime = null;
    const startValue = 0;

    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      setCount(Math.floor(progress * (end - startValue) + startValue));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [end, duration, trigger]);

  return count;
};

const FAQItem = ({ question, answer }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="border border-white/[0.06] bg-white/[0.02] rounded-2xl overflow-hidden transition-all duration-300">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-5 flex items-center justify-between text-left font-bold text-sm tracking-tight text-white hover:bg-white/[0.03] transition cursor-pointer border-none bg-transparent"
      >
        <span>{question}</span>
        {isOpen ? <ChevronUp className="w-4 h-4 text-purple-400" /> : <ChevronDown className="w-4 h-4 text-purple-400" />}
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            className="px-6 pb-5 text-xs text-slate-400 leading-relaxed border-t border-white/[0.04] pt-3 bg-white/[0.01]"
          >
            {answer}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function LandingPage({ onLaunch }) {
  const [activeSection, setActiveSection] = useState("home");
  const performanceRef = useRef(null);
  const [performanceVisible, setPerformanceVisible] = useState(false);

  // Restore body overflow scrollability on mount
  useEffect(() => {
    document.body.style.overflow = "auto";
    return () => {
      document.body.style.overflow = "hidden";
    };
  }, []);

  // Parallax background effect
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX - window.innerWidth / 2) / 35,
        y: (e.clientY - window.innerHeight / 2) / 35,
      });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Performance section visibility observer for counter trigger
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setPerformanceVisible(true);
        }
      },
      { threshold: 0.2 }
    );
    if (performanceRef.current) {
      observer.observe(performanceRef.current);
    }
    return () => observer.disconnect();
  }, []);

  const performanceCounters = {
    offline: useCounter(100, 2000, performanceVisible),
    dimensions: useCounter(768, 2000, performanceVisible),
    stages: useCounter(5, 1500, performanceVisible),
    internet: useCounter(0, 1000, performanceVisible)
  };

  return (
    <div className="bg-[#05030F] text-white min-h-screen font-sans overflow-x-hidden selection:bg-purple-500/30 selection:text-purple-200 scroll-smooth relative">
      {/* Background Neon Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-purple-900/10 blur-[150px] pointer-events-none" />
      <div className="absolute top-[40%] right-[-10%] w-[45vw] h-[45vw] rounded-full bg-violet-900/10 blur-[150px] pointer-events-none" />
      <div className="absolute bottom-[10%] left-[20%] w-[35vw] h-[35vw] rounded-full bg-indigo-900/10 blur-[150px] pointer-events-none" />

      {/* Grid Overlay */}
      <div 
        className="absolute inset-0 bg-[linear-gradient(to_right,#1f1a3a_1px,transparent_1px),linear-gradient(to_bottom,#1f1a3a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-[0.15] pointer-events-none" 
        style={{
          transform: `translate(${mousePosition.x * 0.2}px, ${mousePosition.y * 0.2}px)`
        }}
      />

      {/* ---------------- SECTION 1 — NAVBAR ---------------- */}
      <header className="sticky top-0 z-50 w-full border-b border-white/[0.06] bg-[#05030f]/60 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => window.scrollTo(0, 0)}>
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-violet-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Brain className="w-4.5 h-4.5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">
              Saarthi AI
            </span>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-400">
            {["Home", "Architecture", "Features", "Technology", "Security", "Benefits", "FAQ", "Contact"].map((link) => (
              <a
                key={link}
                href={`#${link.toLowerCase()}`}
                className="hover:text-purple-400 transition-colors duration-200"
              >
                {link}
              </a>
            ))}
          </nav>

          {/* Action Buttons */}
          <div className="flex items-center space-x-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white rounded-lg border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] transition flex items-center space-x-1.5 cursor-pointer"
            >
              <GithubIcon className="w-3.5 h-3.5" />
              <span>GitHub</span>
            </a>
            <button
              onClick={onLaunch}
              className="px-4.5 py-2 text-xs font-bold text-white rounded-lg bg-gradient-to-r from-purple-600 to-violet-500 hover:from-purple-500 hover:to-violet-400 shadow-md shadow-purple-600/25 transition cursor-pointer border-none"
            >
              Launch Saarthi
            </button>
          </div>
        </div>
      </header>

      {/* ---------------- SECTION 2 — HERO ---------------- */}
      <section id="home" className="max-w-7xl mx-auto px-6 py-20 lg:py-28 grid lg:grid-cols-12 gap-16 items-center">
        {/* Left Info Column */}
        <div className="lg:col-span-7 flex flex-col space-y-8">
          {/* Badges Container */}
          <div className="flex flex-wrap gap-2">
            {[
              { text: "Offline First", color: "from-purple-500/20 to-purple-500/5 text-purple-350 border-purple-500/30" },
              { text: "On Device AI", color: "from-violet-500/20 to-violet-500/5 text-violet-300 border-violet-500/30" },
              { text: "Privacy First", color: "from-indigo-500/20 to-indigo-500/5 text-indigo-300 border-indigo-500/30" },
              { text: "Made for India", color: "from-pink-500/20 to-pink-500/5 text-pink-300 border-pink-500/30" }
            ].map((badge, idx) => (
              <motion.div
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                key={idx}
                className={`px-3 py-1 rounded-full border text-[10px] font-bold tracking-wide uppercase bg-gradient-to-r ${badge.color} flex items-center space-x-1.5`}
              >
                <CheckCircle2 className="w-3 h-3 text-purple-400" />
                <span>{badge.text}</span>
              </motion.div>
            ))}
          </div>

          {/* Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight text-white tracking-tight">
            Offline AI Assistant for <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-violet-500 to-indigo-400 filter drop-shadow-sm font-black">
              Medical, Legal & Banking
            </span>{" "}
            Queries
          </h1>

          {/* Description */}
          <p className="text-slate-400 text-base md:text-lg leading-relaxed max-w-xl">
            Saarthi AI is a fully offline, on-device Retrieval Augmented Generation (RAG) platform built specifically for Indian citizens. It provides trusted answers using official government knowledge bases, local LLMs, and multilingual AI.
          </p>

          {/* Action Buttons */}
          <div className="flex items-center space-x-4">
            <button
              onClick={onLaunch}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-violet-500 hover:from-purple-500 hover:to-violet-400 font-bold text-sm tracking-wide flex items-center space-x-2 transition shadow-lg shadow-purple-600/30 cursor-pointer border-none"
            >
              <span>Try Demo</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              className="px-6 py-3 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] text-slate-350 hover:text-white font-bold text-sm tracking-wide transition flex items-center space-x-2 cursor-pointer"
            >
              <GithubIcon className="w-4 h-4" />
              <span>View GitHub</span>
            </a>
          </div>
        </div>

        {/* Right Graphic Column */}
        <div className="lg:col-span-5 flex items-center justify-center relative">
          {/* Neon Glow Mesh Background */}
          <div className="absolute w-72 h-72 rounded-full bg-purple-600/20 blur-[80px] pointer-events-none" />

          {/* Brain Graphic Holder */}
          <motion.div 
            animate={{
              y: [0, -15, 0],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="w-80 h-80 rounded-full border border-purple-500/20 bg-[#0c0a1b]/40 backdrop-blur-2xl flex items-center justify-center relative shadow-inner"
          >
            {/* Pulsing rings */}
            <div className="absolute inset-4 rounded-full border border-purple-500/10 animate-ping opacity-30" />
            <div className="absolute inset-12 rounded-full border border-purple-500/10 animate-pulse" />

            <Brain className="w-36 h-36 text-purple-500/80 filter drop-shadow-[0_0_20px_rgba(139,92,246,0.4)]" />

            {/* Glowing Floating Domain Cards */}
            <motion.div
              animate={{
                y: [0, 8, 0],
                x: [0, -4, 0]
              }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              className="absolute top-2 -left-12 px-4 py-2.5 rounded-xl border border-pink-500/30 bg-pink-950/20 backdrop-blur-md flex items-center space-x-2 shadow-lg"
            >
              <HeartPulse className="w-4 h-4 text-pink-400" />
              <span className="text-xs font-bold tracking-wide">Medical</span>
            </motion.div>

            <motion.div
              animate={{
                y: [0, -10, 0],
                x: [0, 6, 0]
              }}
              transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
              className="absolute top-36 -right-16 px-4 py-2.5 rounded-xl border border-purple-500/30 bg-purple-950/20 backdrop-blur-md flex items-center space-x-2 shadow-lg"
            >
              <Scale className="w-4 h-4 text-purple-400" />
              <span className="text-xs font-bold tracking-wide">Legal</span>
            </motion.div>

            <motion.div
              animate={{
                y: [0, 6, 0],
                x: [0, -6, 0]
              }}
              transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut", delay: 2 }}
              className="absolute bottom-6 -left-8 px-4 py-2.5 rounded-xl border border-violet-500/30 bg-violet-950/20 backdrop-blur-md flex items-center space-x-2 shadow-lg"
            >
              <Landmark className="w-4 h-4 text-violet-400" />
              <span className="text-xs font-bold tracking-wide">Banking</span>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* ---------------- SECTION 3 — TRUST BAR ---------------- */}
      <section className="max-w-7xl mx-auto px-6 py-12">
        <div className="w-full py-6 px-8 rounded-2xl border border-white/[0.05] bg-white/[0.02] backdrop-blur-md flex flex-wrap gap-y-6 gap-x-12 items-center justify-around text-slate-400">
          {[
            { text: "SQLite Database", icon: Database },
            { text: "ChromaDB Store", icon: Server },
            { text: "Source Citations", icon: FileText },
            { text: "Govt Knowledge Base", icon: CheckCircle2 },
            { text: "No Internet Required", icon: Unlock },
            { text: "Session Isolation", icon: Shield }
          ].map((item, idx) => (
            <div key={idx} className="flex items-center space-x-2">
              <item.icon className="w-4 h-4 text-purple-500/70" />
              <span className="text-xs font-bold tracking-wide text-slate-350">{item.text}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- SECTION 4 — HOW SAARTHI AI WORKS ---------------- */}
      <section id="about" className="max-w-7xl mx-auto px-6 py-24 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Process Workflow</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">How Saarthi AI Works</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            The offline RAG ingestion and retrieval architecture guarantees data sovereignty and speed.
          </p>
        </div>

        {/* Timeline Timeline Grid */}
        <div className="grid md:grid-cols-5 gap-6 relative">
          {[
            {
              step: "01",
              title: "Knowledge Base Seeding",
              desc: "Official government PDFs are indexed, parsed, chunked into 512-character blocks, and stored in a vector database.",
              items: ["Government PDF crawling", "Embedding generation", "Vector Database Ingestion"]
            },
            {
              step: "02",
              title: "Upload & OCR",
              desc: "User uploads PDF, DOCX, or images. Document text is extracted, or run through preprocessed Tesseract OCR.",
              items: ["PDF & DOCX parsing", "Autocontrast Image OCR", "Confidence Threshold Warning"]
            },
            {
              step: "03",
              title: "Hybrid Retrieval",
              desc: "Query undergoes Hinglish glossary expansion, retrieves matched vectors, and prioritizes user documents over public base.",
              items: ["Colloquial Glossary", "Dual Collection Search", "Score Normalization & Boost"]
            },
            {
              step: "04",
              title: "Local LLM",
              desc: "Runs context chunks through localized Ollama llama3.2 model. Employs pre-generation domain guardrails.",
              items: ["Llama 3.2 1B Model", "Hallucination Protection", "Inline Reference Citations"]
            },
            {
              step: "05",
              title: "Streaming Output",
              desc: "Delivers generated text via Server-Sent Events. Includes voice input and text-to-speech outputs.",
              items: ["FastAPI SSE Streaming", "Whisper Speech Ingestion", "Offline Voice Synthesis"]
            }
          ].map((item, idx) => (
            <motion.div
              whileHover={{ y: -8 }}
              transition={{ duration: 0.3 }}
              key={idx}
              className="p-6 rounded-2xl border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.04] backdrop-blur-xl flex flex-col space-y-4 relative shadow-lg cursor-pointer"
            >
              {/* Connector line indicator */}
              {idx < 4 && (
                <div className="hidden md:block absolute top-12 right-[-20px] w-[30px] h-[1px] border-t border-dashed border-purple-500/20 z-0" />
              )}
              <span className="text-3xl font-black text-purple-500/35">{item.step}</span>
              <h3 className="text-base font-bold tracking-tight text-white">{item.title}</h3>
              <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
              <div className="flex flex-col space-y-1.5 pt-2">
                {item.items.map((sub, sIdx) => (
                  <div key={sIdx} className="flex items-center space-x-1.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500/70" />
                    <span className="text-[10px] font-medium text-slate-350">{sub}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ---------------- SECTION 5 — DOMAINS ---------------- */}
      <section id="domains" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Knowledge Domains</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Structured Domain Expertise</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Engineered to handle colloquial terminologies and complex governance frameworks.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              title: "Medical",
              desc: "Resolves Hinglish medical queries (e.g., 'bukhar ka ilaj') using official National Health Mission standard treatment guidelines.",
              icon: HeartPulse,
              color: "from-pink-500/10 to-pink-500/0 border-pink-500/25",
              iconColor: "text-pink-400",
              bullets: ["National Health Schemes", "Standard Health Guidelines", "Diseases & Symptom logs", "Essential Medicine lists"]
            },
            {
              title: "Legal",
              desc: "Answers queries regarding legal rights, court filing procedures (e.g. FIR), and the Constitution of India in English/Hindi.",
              icon: Scale,
              color: "from-purple-500/10 to-purple-500/0 border-purple-500/25",
              iconColor: "text-purple-400",
              bullets: ["Constitution of India", "Consumer Protection Acts", "RTI Filing regulations", "Bharatiya Nyaya Sanhita (BNS)"]
            },
            {
              title: "Banking",
              desc: "Explains RBI regulations, home loan foreclosure guidelines, credit card usage rights, and customer grievance options.",
              icon: Landmark,
              color: "from-violet-500/10 to-violet-500/0 border-violet-500/25",
              iconColor: "text-violet-400",
              bullets: ["RBI Master KYC Directions", "Foreclosure & Rate circulars", "Customer Protection Rights", "Digital Banking directives"]
            }
          ].map((card, idx) => (
            <div
              key={idx}
              className={`p-8 rounded-3xl border bg-gradient-to-b ${card.color} flex flex-col space-y-6 relative overflow-hidden`}
            >
              {/* Orb Glow */}
              <div className="absolute -top-12 -right-12 w-28 h-28 rounded-full bg-purple-500/10 blur-[30px]" />
              
              <div className="flex items-center space-x-3.5">
                <div className={`p-3 rounded-2xl bg-white/[0.03] border border-white/[0.08] ${card.iconColor}`}>
                  <card.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold tracking-tight">{card.title}</h3>
              </div>

              <p className="text-slate-400 text-xs leading-relaxed">{card.desc}</p>

              <div className="flex flex-col space-y-2.5 pt-2 border-t border-white/[0.05]">
                {card.bullets.map((b, bIdx) => (
                  <div key={bIdx} className="flex items-center space-x-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-purple-500/70" />
                    <span className="text-xs font-semibold text-slate-300">{b}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- SECTION 6 — SYSTEM ARCHITECTURE ---------------- */}
      <section id="architecture" className="max-w-7xl mx-auto px-6 py-24 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">System Design</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Technical Bento Grid Architecture</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Deep dive into the underlying components that orchestrate Saarthi AI.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Col 1 */}
          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group">
            <div className="flex flex-col space-y-3">
              <Database className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">SQLite</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Manages relational database structures including user sessions, uploads catalog, messaging boards, and API telemetry logs.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Database Engine</span>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group md:col-span-2">
            <div className="flex flex-col space-y-3">
              <Cpu className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">Ollama RAG Engine</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Executes optimized inference calls targeting local Llama 3.2 models on-device. Safe pre-generation check avoids hallucination by comparing Cosine similarity threshold metrics.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Localized Inference</span>
          </div>

          {/* Col 2 */}
          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group md:col-span-2">
            <div className="flex flex-col space-y-3">
              <Layers className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">Hybrid Retrieval</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Leverages Devanagari/Romanized glossary mappings to expand queries, executes dual-collection ChromaDB routing, and applies modular keyword scoring.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Router Pipeline</span>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group">
            <div className="flex flex-col space-y-3">
              <Eye className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">OCR Engine</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Binarizes and preprocesses image files using adaptive median filtering and autocontrast adjustments before running Tesseract OCR.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Optical Recognition</span>
          </div>

          {/* Col 3 */}
          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group">
            <div className="flex flex-col space-y-3">
              <Network className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">FastAPI</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Handles file uploads ingestion, Whisper base model STT, pyttsx3 voice synthesis, SSE streams, and system telemetry logging.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Backend Server</span>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group">
            <div className="flex flex-col space-y-3">
              <Database className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">ChromaDB</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Persistent local vector database that holds public knowledge base embeddings and session-isolated user document chunks.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Vector Database</span>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] hover:border-purple-500/30 hover:scale-[1.01] transition-all duration-300 flex flex-col justify-between h-72 cursor-pointer group">
            <div className="flex flex-col space-y-3">
              <Globe className="w-8 h-8 text-purple-400 group-hover:text-purple-300 transition-colors" />
              <h3 className="text-base font-bold tracking-tight">React Frontend</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Responsive 3-column layout built with React, Vite, and Tailwind. Serves as a single unified client interface served directly from the edge.
              </p>
            </div>
            <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest">Client Web App</span>
          </div>
        </div>
      </section>

      {/* ---------------- SECTION 7 — POWERFUL FEATURES ---------------- */}
      <section id="features" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Product Capability</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Powerful Capabilities at the Edge</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Engineered to exceed critical RAG standards entirely offline.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-2 p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Unlock className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Fully Offline Architecture</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              No internet connection required. Operates perfectly in disconnected or highly secure network areas, safeguarding intellectual property and data sovereignty.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Globe className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Bilingual Translation</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Accepts input and output in Hindi and English seamlessly, translating Hinglish queries automatically.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Mic className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">STT Voice Input</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Voice queries transcribed locally on device using lightweight Whisper base speech models.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Volume2 className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">TTS Speech Output</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Local speech synthesis using pyttsx3 backends with Hindi voice registries configuration.
            </p>
          </div>

          <div className="md:col-span-2 p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <FileText className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Source Citations & references</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Guarantees credibility by providing exact document reference citations (filename, page number, excerpts) mapped dynamically inside message bubbles.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Shield className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Session Isolation</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Uploads and memory traces are isolated by browser session IDs. Automatically purges references on close.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Layers className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Hybrid RAG pipeline</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Combines lexical query boosting, colloquial glossary expansions, and multilingual vector embeddings search.
            </p>
          </div>

          <div className="md:col-span-2 p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Sparkles className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Hallucination Guardrails</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Applies rigid similarity score check threshold (0.60) and queries domain-mismatch tests to safely block model hallucination.
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/[0.06] bg-[#0c0a1b]/40 flex flex-col space-y-4">
            <Cpu className="w-8 h-8 text-purple-400" />
            <h3 className="text-lg font-bold tracking-tight">Jetson Optimization</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Optimized for 15W edge devices (NVIDIA Jetson) using offline hub modes and locked PyTorch dependencies.
            </p>
          </div>
        </div>
      </section>

      {/* ---------------- SECTION 8 — TECHNOLOGY STACK ---------------- */}
      <section id="technology" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Core Technology</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Built on the Best Open-Source Tech</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            A cohesive stack designed for low-latency, cross-platform performance.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {[
            { name: "Python", desc: "Core Logic Engine" },
            { name: "FastAPI", desc: "Asynchronous Server" },
            { name: "React & Vite", desc: "Client Interface" },
            { name: "Tailwind CSS", desc: "Premium Layouts" },
            { name: "SQLite", desc: "Relational Registry" },
            { name: "ChromaDB", desc: "Vector Search Store" },
            { name: "Ollama Llama", desc: "Inference Model" },
            { name: "Whisper Base", desc: "Voice Input STT" },
            { name: "PyMuPDF", desc: "PDF Parsing Engine" },
            { name: "Tesseract OCR", desc: "Image Text Extraction" },
            { name: "NVIDIA Jetson", desc: "Edge Deployment Hardware" },
            { name: "Framer Motion", desc: "Fluid UI Animations" }
          ].map((tech, idx) => (
            <motion.div
              whileHover={{ scale: 1.03, borderColor: "rgba(139, 92, 246, 0.4)" }}
              key={idx}
              className="p-6 rounded-2xl border border-white/[0.05] bg-white/[0.01] flex flex-col items-center justify-center space-y-2 cursor-pointer transition-colors"
            >
              <span className="text-base font-bold text-white tracking-tight">{tech.name}</span>
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">{tech.desc}</span>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ---------------- SECTION 9 — SECURITY ---------------- */}
      <section id="security" className="max-w-7xl mx-auto px-6 py-24 grid lg:grid-cols-2 gap-16 items-center">
        {/* Left Side: Security Cards */}
        <div className="flex flex-col space-y-8">
          <div className="flex flex-col space-y-4">
            <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Privacy First</span>
            <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Strict Data Sovereignty</h2>
            <p className="text-slate-400 text-sm leading-relaxed">
              Every design decision is built around protecting the user's data privacy.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                title: "Upload Isolation",
                desc: "Uploaded documents are dynamically isolated using unique session keys, preventing cross-session visibility.",
                icon: Shield
              },
              {
                title: "Metadata Filtering",
                desc: "Queries strictly target and filter session documents, keeping personal and general context partitioned.",
                icon: Search
              },
              {
                title: "Temporary Cleanup",
                desc: "FastAPI background tasks instantly remove temporary upload files and synthesized speech clips from storage.",
                icon: FileText
              },
              {
                title: "Offline Processing",
                desc: "No telemetry or document data is ever sent to external cloud APIs or networks, preventing accidental data leaks.",
                icon: Unlock
              }
            ].map((item, idx) => (
              <div key={idx} className="p-6 rounded-2xl border border-white/[0.06] bg-white/[0.02] flex flex-col space-y-3">
                <item.icon className="w-5 h-5 text-purple-400" />
                <h3 className="text-sm font-bold tracking-tight text-white">{item.title}</h3>
                <p className="text-slate-400 text-[11px] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: Shield Graphic */}
        <div className="flex items-center justify-center relative">
          {/* Radial Mesh */}
          <div className="absolute w-80 h-80 rounded-full bg-violet-600/15 blur-[90px] pointer-events-none" />
          
          <motion.div
            animate={{
              y: [0, -10, 0],
              rotate: [0, 2, 0]
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="w-72 h-72 rounded-3xl border border-purple-500/25 bg-[#09071c]/30 backdrop-blur-2xl flex items-center justify-center shadow-2xl relative"
          >
            <Shield className="w-32 h-32 text-purple-500/70 filter drop-shadow-[0_0_15px_rgba(139,92,246,0.3)] animate-pulse" />
            <Unlock className="w-8 h-8 text-white absolute top-12 right-12 opacity-60" />
            <CheckCircle2 className="w-6 h-6 text-green-400 absolute bottom-12 left-12 opacity-70" />
          </motion.div>
        </div>
      </section>

      {/* ---------------- SECTION 10 — PERFORMANCE ---------------- */}
      <section ref={performanceRef} className="max-w-7xl mx-auto px-6 py-20">
        <div className="w-full py-16 px-8 rounded-3xl border border-white/[0.05] bg-gradient-to-r from-purple-950/10 via-[#0c0a1b]/40 to-indigo-950/10 backdrop-blur-md grid md:grid-cols-4 gap-8 text-center relative overflow-hidden">
          {/* Decorative mesh */}
          <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none" />

          {[
            { value: performanceCounters.offline, suffix: "%", desc: "Offline Execution" },
            { value: performanceCounters.dimensions, suffix: "D", desc: "Embedding Dimension" },
            { value: performanceCounters.stages, suffix: "", desc: "Processing Stages" },
            { value: performanceCounters.internet, suffix: "", desc: "Internet Required" }
          ].map((item, idx) => (
            <div key={idx} className="flex flex-col space-y-2 relative z-10">
              <span className="text-4xl md:text-5xl lg:text-6xl font-black text-purple-400 tracking-tight">
                {item.value}{item.suffix}
              </span>
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {item.desc}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- BENEFITS SECTION ---------------- */}
      <section id="benefits" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Core Benefits</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Designed for Secure High-Stakes Operations</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Delivering trust, speed, and cost efficiency directly at the operational edge.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              title: "Zero Ingestion Costs",
              desc: "No pay-per-token API charges. Run unlimited queries and ingest thousands of pages entirely free of cloud costs.",
              icon: Sparkles
            },
            {
              title: "100% Data Sovereignty",
              desc: "Patient files, case briefs, and banking circulars remain localized. Absolute compliance with zero network exposure.",
              icon: Shield
            },
            {
              title: "Instant Edge Response",
              desc: "Sub-second retrieval durations and low latency model streaming, bypassing network congestion and API downtimes.",
              icon: Cpu
            },
            {
              title: "Multilingual Voice Support",
              desc: "Accepts speech input and generates offline Hinglish/Hindi text-to-speech answers for diverse accessibility.",
              icon: Mic
            }
          ].map((item, idx) => (
            <div key={idx} className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] flex flex-col space-y-4 relative overflow-hidden group hover:border-purple-500/20 transition-all duration-300">
              <div className="p-3 rounded-2xl bg-white/[0.03] border border-white/[0.08] text-purple-400 w-fit">
                <item.icon className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold tracking-tight text-white">{item.title}</h3>
              <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- FAQ SECTION ---------------- */}
      <section id="faq" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Got Questions?</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Frequently Asked Questions</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Everything you need to know about Saarthi AI's offline operations and integrations.
          </p>
        </div>

        <div className="max-w-3xl flex flex-col space-y-4">
          <FAQItem
            question="Does Saarthi AI require an internet connection?"
            answer="No. Saarthi AI is built to be completely offline-first. Seeding runs once during developer setup to initialize the database and fetch the multilingual embedding model. Afterward, all query routing, dense vector retrieval, and LLM generation runs 100% on-device."
          />
          <FAQItem
            question="What local model does Saarthi AI use?"
            answer="It runs the lightweight llama3.2:1b model via Ollama. It is optimized for speed, low RAM footprints, and low power edge devices."
          />
          <FAQItem
            question="How is data isolation handled?"
            answer="Every upload, document indexing transaction, and conversation history is strictly partitioned by unique session IDs. Our Isolation Guard verifies metadata ownership before retrieval, and FastAPI cleans up temporary workspace files on teardown."
          />
          <FAQItem
            question="Can it be deployed on NVIDIA Jetson?"
            answer="Yes. The architecture includes specific Edge Runtime tuning (like thread optimization, model warmup strategies, and swap control) that makes it run efficiently under 15W boundaries on NVIDIA Jetson platforms."
          />
        </div>
      </section>

      {/* ---------------- CONTACT SECTION ---------------- */}
      <section id="contact" className="max-w-7xl mx-auto px-6 py-20 flex flex-col space-y-16">
        <div className="flex flex-col space-y-4 max-w-xl mx-auto text-center">
          <span className="text-xs font-bold tracking-wider text-purple-400 uppercase">Support & Queries</span>
          <h2 className="text-3xl md:text-4xl font-extrabold tracking-tight">Connect With Saarthi AI</h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Get in touch for enterprise deployment packages, custom seeding models, and hardware integrations.
          </p>
        </div>

        <div className="max-w-4xl mx-auto w-full grid md:grid-cols-3 gap-8">
          {[
            { label: "Mail Us", value: "support@saarthi.ai", sub: "Enterprise inquiries", icon: Mail },
            { label: "Call Us", value: "+91 11 2345 6789", sub: "Mon-Fri, 9am - 6pm", icon: Phone },
            { label: "Visit Us", value: "Digital India Hub, Delhi", sub: "Innovation Enclave", icon: MapPin }
          ].map((card, idx) => (
            <div key={idx} className="p-8 rounded-3xl border border-white/[0.06] bg-white/[0.02] flex flex-col items-center text-center space-y-4 hover:border-purple-500/20 transition-all duration-300">
              <div className="p-3 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400">
                <card.icon className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">{card.label}</span>
                <h4 className="text-sm font-bold text-white">{card.value}</h4>
                <p className="text-slate-400 text-[10px]">{card.sub}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- SECTION 11 — FINAL CTA ---------------- */}
      <section className="max-w-7xl mx-auto px-6 py-24 relative overflow-hidden">
        {/* Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-purple-600/15 blur-[120px] pointer-events-none" />
        
        <div className="max-w-3xl mx-auto py-20 px-8 rounded-3xl border border-purple-500/20 bg-gradient-to-b from-[#0e0a25] to-[#05030f] backdrop-blur-xl flex flex-col items-center text-center space-y-8 relative shadow-2xl">
          <div className="p-4 rounded-full bg-purple-500/15 border border-purple-500/25">
            <Brain className="w-8 h-8 text-purple-400" />
          </div>

          <h2 className="text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight max-w-lg leading-tight">
            Ready to Experience Offline AI?
          </h2>

          <p className="text-slate-400 text-sm max-w-md leading-relaxed">
            Built specifically for India. Private. Reliable. Operating completely at the edge.
          </p>

          <div className="flex flex-col sm:flex-row items-center gap-4">
            <button
              onClick={onLaunch}
              className="px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-violet-500 hover:from-purple-500 hover:to-violet-400 font-bold text-sm tracking-wide transition shadow-lg shadow-purple-600/30 cursor-pointer border-none text-white"
            >
              Launch Saarthi
            </button>
            <a
              href="#about"
              className="px-8 py-3.5 rounded-xl border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.06] text-slate-300 hover:text-white font-bold text-sm tracking-wide transition cursor-pointer"
            >
              Explore Documentation
            </a>
          </div>
        </div>
      </section>

      {/* ---------------- SECTION 12 — FOOTER ---------------- */}
      <footer className="border-t border-white/[0.06] bg-[#030209] py-16 text-slate-500 text-xs">
        <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-12">
          {/* Col 1 */}
          <div className="flex flex-col space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-md bg-purple-600 flex items-center justify-center">
                <Brain className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="font-bold text-sm tracking-tight text-white">Saarthi AI</span>
            </div>
            <p className="text-[11px] leading-relaxed text-slate-400">
              Offline RAG assistant platform engineered for low latency on edge device hardware.
            </p>
            <span className="text-[10px] text-slate-500">© 2026 Saarthi AI. All rights reserved.</span>
          </div>

          {/* Col 2 */}
          <div className="flex flex-col space-y-3">
            <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">Product</span>
            {["Overview", "Timeline", "Architecture", "Domains"].map((item) => (
              <a key={item} href={`#${item.toLowerCase()}`} className="hover:text-purple-400 transition-colors">
                {item}
              </a>
            ))}
          </div>

          {/* Col 3 */}
          <div className="flex flex-col space-y-3">
            <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">Technology</span>
            {["FastAPI Backend", "React Frontend", "Ollama Llama", "ChromaDB Store"].map((item) => (
              <span key={item} className="text-slate-400">
                {item}
              </span>
            ))}
          </div>

          {/* Col 4 */}
          <div className="flex flex-col space-y-3">
            <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">Resources</span>
            <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-purple-400 transition-colors flex items-center space-x-1">
              <GithubIcon className="w-3.5 h-3.5" />
              <span>GitHub Repository</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
