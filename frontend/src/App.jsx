import React, { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import { Brain } from "lucide-react";
import Sidebar from "./components/layout/Sidebar";
import ChatWorkspace from "./components/layout/ChatWorkspace";
import CitationDrawer from "./components/CitationDrawer";
import LandingPage from "./components/LandingPage";
import { useTheme } from "./hooks/useTheme";
import { useKeyboardShortcuts } from "./hooks/useKeyboardShortcuts";
import { translations } from "./utils/localization";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [view, setView] = useState("app");
  const [masterSessionId, setMasterSessionId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [documentsList, setDocumentsList] = useState([]);
  
  const [refreshList, setRefreshList] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [appLoading, setAppLoading] = useState(true);
  const [newChatTrigger, setNewChatTrigger] = useState(0);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  // Theme & Language states
  const { theme, toggleTheme } = useTheme();
  const [language, setLanguage] = useState(() => localStorage.getItem("saarthi_language") || "en");

  const t = translations[language] || translations.en;

  // Track language changes
  useEffect(() => {
    localStorage.setItem("saarthi_language", language);
  }, [language]);

  // Fetch document history at top-level to sync search, sidebar manager, input box suggestions, and chat header
  const fetchDocuments = async (session_id, conversation_id) => {
    if (!session_id) return;
    try {
      const url = `${API_BASE}/api/history?session_id=${session_id}${
        conversation_id ? `&conversation_id=${conversation_id}` : ""
      }`;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setDocumentsList(data.documents || []);
      }
    } catch (err) {
      console.error("Failed to fetch documents list:", err);
    }
  };

  const fetchConversations = async () => {
    try {
      const deviceId = localStorage.getItem("saarthi_device_id");
      if (!deviceId) return [];
      const response = await fetch(`${API_BASE}/api/conversations/all?device_id=${deviceId}`);
      if (response.ok) {
        const data = await response.json();
        const convs = data.conversations || [];
        setConversations(convs);
        return convs;
      }
    } catch (err) {
      console.error("Failed to fetch conversations:", err);
    }
    return [];
  };

  // Keyboard Shortcuts Hook
  useKeyboardShortcuts({
    onNewChat: () => handleNewChat(),
    onSearch: () => {
      // Focus search input
      const searchInput = document.querySelector('input[type="text"]');
      searchInput?.focus();
    },
    onEscape: () => {
      setIsDrawerOpen(false);
    }
  });

  // Initialize master session and active thread
  useEffect(() => {
    const initializeApp = async () => {
      let deviceId = localStorage.getItem("saarthi_device_id");
      if (!deviceId) {
        deviceId = `dev_${Math.random().toString(36).substring(2, 15)}`;
        localStorage.setItem("saarthi_device_id", deviceId);
      }

      let storedMasterSession = localStorage.getItem("saarthi_master_session_id");
      if (!storedMasterSession) {
        storedMasterSession = `usr_${Math.random().toString(36).substring(2, 10)}`;
        localStorage.setItem("saarthi_master_session_id", storedMasterSession);
      }
      setMasterSessionId(storedMasterSession);

      // Fetch conversations list
      const list = await fetchConversations();
      
      let storedActiveConv = localStorage.getItem("saarthi_active_conversation_id");
      if (storedActiveConv === "new") {
        setActiveConversationId("new");
      } else if (storedActiveConv && list.some(c => c.id === storedActiveConv)) {
        setActiveConversationId(storedActiveConv);
        loadMessages(storedActiveConv);
      } else if (list.length > 0) {
        const recentConvId = list[0].id;
        setActiveConversationId(recentConvId);
        localStorage.setItem("saarthi_active_conversation_id", recentConvId);
        loadMessages(recentConvId);
      } else {
        setActiveConversationId("new");
        localStorage.setItem("saarthi_active_conversation_id", "new");
      }
      setAppLoading(false);
    };

    initializeApp();
  }, []);

  // Update documents list on session/conversation/refresh switch
  useEffect(() => {
    if (masterSessionId && activeConversationId) {
      if (activeConversationId === "new") {
        setDocumentsList([]);
      } else {
        fetchDocuments(masterSessionId, activeConversationId);
      }
    }
  }, [masterSessionId, activeConversationId, refreshList]);

  const loadMessages = async (convId) => {
    try {
      const response = await fetch(`${API_BASE}/api/conversations/${convId}/messages`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      }
    } catch (err) {
      console.error("Failed to load messages:", err);
    }
  };



  const handleConversationClick = async (convId) => {
    setActiveConversationId(convId);
    localStorage.setItem("saarthi_active_conversation_id", convId);
    setIsDrawerOpen(false);
    setSelectedCitation(null);
    setRefreshList(prev => !prev);
    loadMessages(convId);
  };

  const handleNewChat = () => {
    setActiveConversationId("new");
    localStorage.setItem("saarthi_active_conversation_id", "new");
    setIsDrawerOpen(false);
    setSelectedCitation(null);
    setMessages([]); // Clear messages for a new chat
    setNewChatTrigger(prev => prev + 1);
  };

  const handleRenameConversation = async (convId, newTitle) => {
    try {
      const response = await fetch(`${API_BASE}/api/conversations/${convId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle }),
      });
      if (response.ok) {
        fetchConversations();
      }
    } catch (err) {
      console.error("Failed to rename conversation:", err);
    }
  };

  const handleDeleteConversation = async (convId) => {
    try {
      const response = await fetch(`${API_BASE}/api/conversations/${convId}?session_id=${masterSessionId}`, {
        method: "DELETE",
      });
      if (response.ok) {
        const updatedList = await fetchConversations();
        if (activeConversationId === convId) {
          if (updatedList.length > 0) {
            const nextConvId = updatedList[0].id;
            setActiveConversationId(nextConvId);
            localStorage.setItem("saarthi_active_conversation_id", nextConvId);
            loadMessages(nextConvId);
          } else {
            setActiveConversationId("new");
            localStorage.setItem("saarthi_active_conversation_id", "new");
            setMessages([]);
          }
        }
        setRefreshList(prev => !prev);
      }
    } catch (err) {
      console.error("Failed to delete conversation:", err);
    }
  };

  const handleDeleteDocument = async (docId) => {
    if (!masterSessionId) return;
    try {
      const response = await fetch(`${API_BASE}/api/document/${docId}?session_id=${masterSessionId}`, {
        method: "DELETE"
      });
      if (response.ok) {
        setRefreshList(prev => !prev);
      }
    } catch (err) {
      console.error("Failed to delete document:", err);
    }
  };

  const handleCitationClick = (citation) => {
    setSelectedCitation(citation);
    setIsDrawerOpen(true);
  };

  const handleCloseDrawer = () => {
    setIsDrawerOpen(false);
  };

  const onMessageSent = () => {
    if (masterSessionId) {
      fetchConversations(masterSessionId);
    }
  };

  if (appLoading) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center relative overflow-hidden"
        style={{ background: "var(--bg-primary)" }}
      >
        <div className="grid-overlay absolute inset-0 opacity-[0.06] pointer-events-none" />
        <div className="flex flex-col items-center space-y-6 relative z-10 select-none text-center">
          <div 
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-white shadow-lg animate-pulse-glow"
            style={{ background: "var(--accent-gradient)" }}
          >
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div className="space-y-1.5">
            <h1 className="text-sm font-black tracking-widest text-gradient">
              SARTHI AI
            </h1>
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider animate-pulse">
              {language === "hi" ? "आरंभ हो रहा है..." : "Initializing offline environment..."}
            </span>
          </div>
        </div>
      </div>
    );
  }

  if (view === "landing") {
    return <LandingPage onLaunch={() => setView("app")} />;
  }

  return (
    <div 
      className="h-screen w-screen flex overflow-hidden font-sans relative"
      style={{ background: "var(--bg-primary)", color: "var(--text-primary)" }}
    >
      {/* Grid overlay pattern inside app */}
      <div className="grid-overlay absolute inset-0 opacity-[0.06] pointer-events-none z-0" />

      {/* Left Sidebar */}
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onConversationClick={(id) => {
          handleConversationClick(id);
          setIsMobileSidebarOpen(false);
        }}
        onNewChat={() => {
          handleNewChat();
          setIsMobileSidebarOpen(false);
        }}
        onDeleteConversation={handleDeleteConversation}
        onRenameConversation={handleRenameConversation}
        sessionId={masterSessionId}
        conversationId={activeConversationId}
        refreshTrigger={refreshList}
        language={language}
        setLanguage={setLanguage}
        theme={theme}
        toggleTheme={toggleTheme}
        documentsList={documentsList}
        onBackToLanding={() => setView("landing")}
        isMobileOpen={isMobileSidebarOpen}
        onCloseMobile={() => setIsMobileSidebarOpen(false)}
      />

      {/* Main Workspace chat panel */}
      <main className="flex-1 flex flex-col overflow-hidden relative z-10">
        <ChatWorkspace
          sessionId={masterSessionId}
          conversationId={activeConversationId}
          messages={messages}
          setMessages={setMessages}
          onCitationClick={handleCitationClick}
          onMessageSent={onMessageSent}
          onUploadSuccess={() => setRefreshList(prev => !prev)}
          language={language}
          conversations={conversations}
          onRenameConversation={handleRenameConversation}
          documentsList={documentsList}
          onDeleteDocument={handleDeleteDocument}
          onConversationCreated={(newId) => {
            setActiveConversationId(newId);
            localStorage.setItem("saarthi_active_conversation_id", newId);
            fetchConversations();
          }}
          newChatTrigger={newChatTrigger}
          onToggleMobileSidebar={() => setIsMobileSidebarOpen(prev => !prev)}
        />
      </main>

      {/* Citation slide-in drawer */}
      <CitationDrawer
        citation={selectedCitation}
        isOpen={isDrawerOpen}
        onClose={handleCloseDrawer}
        language={language}
      />
    </div>
  );
}
