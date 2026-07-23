import React, { useState, useEffect, useRef } from "react";
import { ArrowDown, Upload, X } from "lucide-react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "../chat/ChatMessages";
import InputArea from "../chat/InputArea";
import CameraModal from "../chat/CameraModal";
import TypingIndicator from "../chat/TypingIndicator";
import { translations } from "../../utils/localization";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatWorkspace({
  sessionId,
  conversationId,
  messages,
  setMessages,
  onCitationClick,
  onMessageSent,
  onUploadSuccess,
  language,
  conversations,
  onRenameConversation,
  documentsList,
  onDeleteDocument,
  onConversationCreated,
  newChatTrigger,
  onToggleMobileSidebar
}) {
  const t = translations[language] || translations.en;
  
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentStreamText, setCurrentStreamText] = useState("");
  const [streamCitations, setStreamCitations] = useState([]);
  
  const [attachedFile, setAttachedFile] = useState(null);
  
  const inputRef = useRef(input);
  useEffect(() => { inputRef.current = input; }, [input]);
  const attachedFileRef = useRef(attachedFile);
  useEffect(() => { attachedFileRef.current = attachedFile; }, [attachedFile]);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [uploadStep, setUploadStep] = useState(0);
  const [uploadError, setUploadError] = useState(null);
  const [inlineError, setInlineError] = useState(null);
  
  const [cameraOpen, setCameraOpen] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [showScrollBottom, setShowScrollBottom] = useState(false);
  const [isDragActive, setIsDragActive] = useState(false);

  const fileInputRef = useRef(null);
  const photoInputRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const messagesEndRef = useRef(null);
  const activeStreamsRef = useRef({});
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const textareaRef = useRef(null);

  // Check scroll position to show/hide floating bottom button
  const handleScroll = (e) => {
    const { scrollTop, scrollHeight, clientHeight } = e.target;
    if (scrollHeight - scrollTop - clientHeight > 200) {
      setShowScrollBottom(true);
    } else {
      setShowScrollBottom(false);
    }
  };

  const scrollToBottom = (behavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  useEffect(() => {
    scrollToBottom("auto");
  }, [conversationId]);

  useEffect(() => {
    scrollToBottom("auto");
  }, [messages, currentStreamText]);

  const prevConvIdRef = useRef(conversationId);
  const draftsRef = useRef({});
  const inTransitConvIdRef = useRef(null);

  useEffect(() => {
    if (newChatTrigger > 0) {
      if (conversationId === "new") {
        setInput("");
        setAttachedFile(null);
      }
      draftsRef.current["new"] = { input: "", attachedFile: null };
    }
  }, [newChatTrigger, conversationId]);

  // Reset local state on conversation change
  useEffect(() => {
    if (inTransitConvIdRef.current === conversationId) {
      inTransitConvIdRef.current = null;
      prevConvIdRef.current = conversationId;
      return;
    }

    draftsRef.current[prevConvIdRef.current] = {
      input: inputRef.current,
      attachedFile: attachedFileRef.current
    };

    const savedDraft = draftsRef.current[conversationId] || { input: "", attachedFile: null };
    setInput(savedDraft.input);
    setAttachedFile(savedDraft.attachedFile);

    setUploadStep(0);
    setUploadError(null);
    setInlineError(null);
    setUploadingFile(false);
    
    // Check if there is an active background stream running for this conversation
    const activeStream = activeStreamsRef.current[conversationId];
    if (activeStream) {
      setIsStreaming(true);
      setCurrentStreamText(activeStream.accumulatedText);
      setStreamCitations(activeStream.accumulatedCitations);
    } else {
      setIsStreaming(false);
      setCurrentStreamText("");
      setStreamCitations([]);
    }
    
    setTranscribing(false);
    setIsRecording(false);
    
    // Do NOT close eventSource here to allow background generation

    prevConvIdRef.current = conversationId;
  }, [conversationId]);

  // Drag and Drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const ensureConversationExists = async (titleHint) => {
    if (conversationId !== "new") return conversationId;
    if (inTransitConvIdRef.current) return inTransitConvIdRef.current;
    
    const words = titleHint.trim().split(/\s+/);
    const title = words.length > 0 ? words.slice(0, 6).join(" ") : "New Conversation";
    
    try {
      const resp = await fetch(`${API_BASE}/api/conversations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, title: title, device_id: localStorage.getItem("saarthi_device_id") })
      });
      if (resp.ok) {
        const data = await resp.json();
        const newConvId = data.conversation_id;
        inTransitConvIdRef.current = newConvId;
        if (onConversationCreated) onConversationCreated(newConvId);
        return newConvId;
      }
    } catch (e) {
      console.error("Failed to lazily create chat:", e);
    }
    return null;
  };

  const validateAndSetFile = async (file) => {
    setInlineError(null);
    setUploadError(null);
    const maxSize = 15 * 1024 * 1024;
    if (file.size > maxSize) {
      setInlineError("File exceeds maximum size limit of 15MB.");
      return;
    }
    
    // Extensions check
    const validExtensions = [".pdf", ".docx", ".jpg", ".jpeg", ".png", ".webp", ".txt"];
    const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (!validExtensions.includes(ext)) {
      setInlineError(`Unsupported file type. Allowed: ${validExtensions.join(", ")}`);
      return;
    }
    
    setAttachedFile(file);
    
    // Start upload immediately
    const targetConvId = await ensureConversationExists(file.name);
    if (targetConvId) {
      await uploadFile(file, targetConvId);
    }
  };

  // Perform upload logic
  const uploadFile = async (fileToUpload, targetConvId) => {
    if (!fileToUpload) return false;
    
    setUploadingFile(true);
    setUploadError(null);
    setUploadStep(0); // Uploading
    
    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("session_id", sessionId);
    if (targetConvId && targetConvId !== "new") {
      formData.append("conversation_id", targetConvId);
    }

    try {
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.message || "File upload failed");
      }

      if (result.job_id) {
        let isDone = false;
        while (!isDone) {
          await new Promise(res => setTimeout(res, 1500));
          const jobRes = await fetch(`${API_BASE}/api/uploads/${result.job_id}`);
          if (jobRes.ok) {
            const jobData = await jobRes.json();
            if (jobData.status === "completed" || jobData.status === "indexed") {
              isDone = true;
              setUploadStep(4);
            } else if (jobData.status === "failed") {
              throw new Error(jobData.error_message || "Document processing failed");
            } else {
              const p = jobData.progress || 0;
              if (p > 0 && p < 40) setUploadStep(1);
              else if (p >= 40 && p < 60) setUploadStep(2);
              else if (p >= 60) setUploadStep(3);
            }
          }
        }
      }

      setUploadStep(4); // Ready
      
      // Delay success reset so timeline shows complete state briefly
      setTimeout(() => {
        setUploadingFile(false);
      }, 1000);

      onUploadSuccess?.();
      return true;
    } catch (err) {
      console.error("Upload error:", err);
      setUploadError(err.message || "An error occurred during file upload.");
      setUploadStep(0);
      setUploadingFile(false);
      return false;
    }
  };

  // Handle message send
  const handleSend = async () => {
    if (isStreaming || uploadingFile || transcribing || isRecording) return;
    
    let currentInput = input;
    if (!currentInput.trim() && !attachedFile) return;

    setInput("");
    
    const activeConvId = await ensureConversationExists(currentInput || "Document Question");
    if (!activeConvId) return;

    // Clear attached file now that we are sending the message
    if (attachedFile) {
      setAttachedFile(null);
      setUploadStep(0);
    }

    // Auto-rename if first message for existing blank conversations
    if (messages.length === 0 && currentInput.trim() && activeConvId === conversationId && activeConvId !== "new") {
      const words = currentInput.trim().split(/\s+/);
      const newTitle = words.slice(0, 6).join(" ");
      if (activeConvId && onRenameConversation) {
        onRenameConversation(activeConvId, newTitle);
      }
    }

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: currentInput }]);
    setIsStreaming(true);
    setCurrentStreamText("");
    setStreamCitations([]);

    const url = `${API_BASE}/api/stream?query=${encodeURIComponent(currentInput)}&session_id=${sessionId}&conversation_id=${activeConvId}`;
    
    const eventSource = new EventSource(url);

    activeStreamsRef.current[activeConvId] = {
      eventSource,
      accumulatedText: "",
      accumulatedCitations: [],
      accumulatedLanguage: "English"
    };

    eventSource.onmessage = (event) => {
      const activeStream = activeStreamsRef.current[activeConvId];
      if (!activeStream) return;

      if (event.data === "[DONE]") {
        eventSource.close();
        delete activeStreamsRef.current[activeConvId];
        
        if (activeConvId === prevConvIdRef.current) {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: activeStream.accumulatedText,
              citations: activeStream.accumulatedCitations,
              response_language: activeStream.accumulatedLanguage,
            },
          ]);
          setCurrentStreamText("");
          setStreamCitations([]);
          setIsStreaming(false);
        }
        onMessageSent?.();
        return;
      }

      try {
        const data = JSON.parse(event.data);
        if (data.skipped_llm) {
          activeStream.accumulatedText = data.answer || "";
          activeStream.accumulatedCitations = data.citations || [];
          activeStream.accumulatedLanguage = data.response_language || "English";
          if (activeConvId === prevConvIdRef.current) {
            setCurrentStreamText(activeStream.accumulatedText);
          }
        } else if (data.type === "token") {
          activeStream.accumulatedText += data.data.token;
          if (activeConvId === prevConvIdRef.current) {
            setCurrentStreamText(activeStream.accumulatedText);
          }
        } else if (data.type === "citation") {
          activeStream.accumulatedCitations = data.data.citations || [];
          if (data.data.validated_text && data.data.validated_text.length >= activeStream.accumulatedText.length) {
            activeStream.accumulatedText = data.data.validated_text;
            if (activeConvId === prevConvIdRef.current) {
              setCurrentStreamText(activeStream.accumulatedText);
            }
          }
          if (activeConvId === prevConvIdRef.current) {
            setStreamCitations(activeStream.accumulatedCitations);
          }
        } else if (data.type === "done") {
          activeStream.accumulatedLanguage = data.data.response_language || "English";
        } else if (data.type === "error") {
          eventSource.close();
          delete activeStreamsRef.current[activeConvId];
          
          if (activeConvId === prevConvIdRef.current) {
            setMessages((prev) => [
              ...prev,
              {
                role: "error",
                content: data.data.message + "\n\n" + (data.data.detail || ""),
              },
            ]);
            setCurrentStreamText("");
            setStreamCitations([]);
            setIsStreaming(false);
          }
          onMessageSent?.();
          return;
        }
      } catch (err) {
        console.error("SSE JSON parse error:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("EventSource error:", err);
      eventSource.close();
      const activeStream = activeStreamsRef.current[activeConvId];
      delete activeStreamsRef.current[activeConvId];
      
      if (activeConvId === prevConvIdRef.current) {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: (activeStream ? activeStream.accumulatedText : "") || "Connection interrupted. Please try again.",
            citations: activeStream ? activeStream.accumulatedCitations : [],
            response_language: activeStream ? activeStream.accumulatedLanguage : "English",
          },
        ]);
        setCurrentStreamText("");
        setStreamCitations([]);
        setIsStreaming(false);
      }
      onMessageSent?.();
    };
  };

  const handleStopStreaming = () => {
    const activeStream = activeStreamsRef.current[conversationId];
    if (activeStream && activeStream.eventSource) {
      activeStream.eventSource.close();
    }
    delete activeStreamsRef.current[conversationId];

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: currentStreamText || "Generation stopped.",
        citations: streamCitations,
      },
    ]);
    setCurrentStreamText("");
    setStreamCitations([]);
    setIsStreaming(false);
    onMessageSent?.();
  };

  // voice / recording logic
  const toggleRecording = async () => {
    setInlineError(null);
    if (isRecording) {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
      setIsRecording(false);
    } else {
      audioChunksRef.current = [];
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        let options = { mimeType: "audio/webm" };
        let mediaRecorder;
        try {
          mediaRecorder = new MediaRecorder(stream, options);
        } catch (e) {
          mediaRecorder = new MediaRecorder(stream);
        }
        
        mediaRecorderRef.current = mediaRecorder;
        mediaRecorder.ondataavailable = (event) => {
          if (event.data && event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };
        
        mediaRecorder.onstop = async () => {
          stream.getTracks().forEach((track) => track.stop());
          const audioBlob = new Blob(audioChunksRef.current, { type: mediaRecorder.mimeType || "audio/webm" });
          if (audioBlob.size === 0) return;
          
          setTranscribing(true);
          const formData = new FormData();
          formData.append("audio", audioBlob, "audio.webm");
          formData.append("lang", language === "en" ? "en" : "hi");
          
          try {
            const response = await fetch(`${API_BASE}/api/voice/transcribe`, {
              method: "POST",
              body: formData,
            });
            
            if (!response.ok) {
              throw new Error("Transcription server error");
            }
            
            const data = await response.json();
            if (data.transcript) {
              setInput((prev) => (prev ? prev + " " + data.transcript : data.transcript));
            }
          } catch (err) {
            console.error("STT error:", err);
            setInlineError("Voice input transcription failed.");
          } finally {
            setTranscribing(false);
          }
        };
        
        mediaRecorder.start();
        setIsRecording(true);
      } catch (err) {
        setInlineError("Cannot access microphone.");
      }
    }
  };

  // message operations
  const handleDeleteMessage = async (idx) => {
    const updated = messages.filter((_, i) => i !== idx);
    setMessages(updated);
  };

  const handleEditMessage = async (idx, newContent) => {
    // Trim history after this message index
    const trimmedMessages = messages.slice(0, idx);
    setMessages(trimmedMessages);
    
    // Trigger sending again with new text
    setInput(newContent);
    setTimeout(() => {
      handleSend();
    }, 50);
  };

  const handleRegenerateMessage = (idx) => {
    // Find the last user query before this index
    let lastQuery = "";
    for (let i = idx - 1; i >= 0; i--) {
      if (messages[i].role === "user") {
        lastQuery = messages[i].content;
        break;
      }
    }
    
    if (lastQuery) {
      // Clear assistant response and re-send
      setMessages(messages.slice(0, idx));
      setInput(lastQuery);
      setTimeout(() => {
        handleSend();
      }, 50);
    }
  };

  return (
    <div 
      className="flex-1 flex flex-col overflow-hidden relative"
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
    >
      {/* Drag & Drop overlay */}
      {isDragActive && (
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-40 flex items-center justify-center p-6 transition">
          <div className="drop-zone active w-full h-full flex flex-col items-center justify-center space-y-4">
            <Upload className="text-purple-500 animate-bounce" size={48} />
            <p className="text-sm font-bold text-white">{t.dropFileHere}</p>
          </div>
        </div>
      )}

      {/* Hidden file inputs */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={(e) => e.target.files?.[0] && validateAndSetFile(e.target.files[0])}
        className="hidden"
        accept=".pdf,.docx"
      />
      <input
        type="file"
        ref={photoInputRef}
        onChange={(e) => e.target.files?.[0] && validateAndSetFile(e.target.files[0])}
        className="hidden"
        accept="image/*"
      />

      <ChatHeader
        activeConversationId={conversationId}
        conversations={conversations}
        onRenameConversation={onRenameConversation}
        documentsCount={documentsList ? documentsList.length : 0}
        language={language}
        onToggleMobileSidebar={onToggleMobileSidebar}
      />

      {/* Messages area wrapper */}
      <div 
        ref={messagesContainerRef} 
        onScroll={handleScroll}
        className="flex-1 flex flex-col overflow-hidden"
      >
        {/* Render uploaded documents at the top of the chat area */}
        {documentsList && documentsList.length > 0 && (
          <div className="px-6 py-4 max-w-2xl mx-auto w-full border-b" style={{ borderColor: "var(--border)" }}>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-2">
              {language === "hi" ? "संलग्न दस्तावेज" : "Conversation Documents"} ({documentsList.length})
            </span>
            <div className="flex flex-wrap gap-2">
              {documentsList.map((doc) => (
                <div key={doc.document_id} className="flex items-center space-x-2 bg-white/5 border px-3 py-2 rounded-xl text-xs max-w-xs truncate shadow-sm animate-fade-in" style={{ borderColor: "var(--border)" }}>
                  <svg className="w-4 h-4 text-purple-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M4 4a2 2 0 012-2h4.586A1 1 0 0112 2.586L15.414 6A1 1 0 0116 6.586V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" />
                  </svg>
                  <span className="truncate flex-1 font-semibold" style={{ color: "var(--text-primary)" }}>
                    {doc.original_filename}
                  </span>
                  <span className="bg-green-500/20 text-green-400 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">
                    Ready
                  </span>
                  <button
                    type="button"
                    onClick={() => onDeleteDocument?.(doc.document_id)}
                    className="text-slate-500 hover:text-red-400 transition cursor-pointer border-none bg-transparent p-0 flex-shrink-0"
                    title="Remove document"
                  >
                    <X size={14} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <ChatMessages
          messages={messages}
          onCitationClick={onCitationClick}
          onSuggestionClick={(q) => {
            setInput(q);
            textareaRef.current?.focus();
          }}
          recentDocs={documentsList}
          language={language}
          onDeleteMessage={handleDeleteMessage}
          onEditMessage={handleEditMessage}
          onRegenerateMessage={handleRegenerateMessage}
          messagesEndRef={messagesEndRef}
        />
        
        {/* Streaming Typings indicator */}
        {isStreaming && (
          <div className="px-6 max-w-2xl mx-auto w-full">
            <TypingIndicator
              streamText={currentStreamText}
              streamCitations={streamCitations}
              onCitationClick={onCitationClick}
              language={language}
            />
          </div>
        )}
        
        {/* Scroll to bottom floating button */}
        {showScrollBottom && (
          <button
            onClick={() => scrollToBottom()}
            className="absolute bottom-6 right-1/2 translate-x-1/2 p-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-full shadow-lg border cursor-pointer z-50 text-white transition-all animate-fade-in"
            style={{ borderColor: "var(--border)" }}
          >
            <ArrowDown size={16} />
          </button>
        )}
      </div>

      <div className="p-4" style={{ background: "var(--bg-primary)" }}>
        <InputArea
          input={input}
          setInput={setInput}
          isStreaming={isStreaming}
          transcribing={transcribing}
          isRecording={isRecording}
          uploadingFile={uploadingFile}
          attachedFile={attachedFile}
          setAttachedFile={setAttachedFile}
          inlineError={inlineError}
          setInlineError={setInlineError}
          onSend={handleSend}
          onStopStreaming={handleStopStreaming}
          toggleRecording={toggleRecording}
          triggerDocUpload={() => fileInputRef.current?.click()}
          triggerPhotoUpload={() => photoInputRef.current?.click()}
          triggerCameraOpen={() => setCameraOpen(true)}
          documentsList={documentsList}
          onDeleteDocument={onDeleteDocument}
          language={language}
        />
      </div>

      {/* Camera Capture Modal */}
      <CameraModal
        isOpen={cameraOpen}
        onClose={() => setCameraOpen(false)}
        onCapture={(file) => {
          setAttachedFile(file);
          setInlineError(null);
        }}
        language={language}
      />

    </div>
  );
}
