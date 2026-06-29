import React, { useState, useEffect, useRef } from "react";
import { ArrowDown, Upload } from "lucide-react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "../chat/ChatMessages";
import InputArea from "../chat/InputArea";
import CameraModal from "../chat/CameraModal";
import UploadTimeline from "../shared/UploadTimeline";
import TypingIndicator from "../chat/TypingIndicator";
import { translations } from "../../utils/localization";

const API_BASE = "http://localhost:8000";

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
  documentsList
}) {
  const t = translations[language] || translations.en;
  
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentStreamText, setCurrentStreamText] = useState("");
  const [streamCitations, setStreamCitations] = useState([]);
  
  const [attachedFile, setAttachedFile] = useState(null);
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
  const eventSourceRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

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
    scrollToBottom();
  }, [messages, currentStreamText]);

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

  const validateAndSetFile = (file) => {
    setInlineError(null);
    setUploadError(null);
    const maxSize = 15 * 1024 * 1024;
    if (file.size > maxSize) {
      setInlineError("File exceeds maximum size limit of 15MB.");
      return;
    }
    
    // Extensions check
    const validExtensions = [".pdf", ".docx", ".jpg", ".jpeg", ".png", ".webp"];
    const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (!validExtensions.includes(ext)) {
      setInlineError(`Unsupported file type. Allowed: ${validExtensions.join(", ")}`);
      return;
    }
    
    setAttachedFile(file);
  };

  // Perform upload logic
  const uploadFile = async (fileToUpload) => {
    if (!fileToUpload) return false;
    
    setUploadingFile(true);
    setUploadError(null);
    setUploadStep(0); // Uploading
    
    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("session_id", sessionId);
    if (conversationId) {
      formData.append("conversation_id", conversationId);
    }

    try {
      // Simulate timelines (actual endpoint handles all in one go, so we transition gracefully)
      const stepTimer = setInterval(() => {
        setUploadStep((prev) => (prev < 3 ? prev + 1 : prev));
      }, 1500);

      const response = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        body: formData,
      });

      clearInterval(stepTimer);
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || "File upload failed");
      }

      setUploadStep(4); // Ready
      setAttachedFile(null);
      
      // Delay success reset so timeline shows complete state briefly
      setTimeout(() => {
        setUploadingFile(false);
        setUploadStep(0);
      }, 1000);

      onUploadSuccess?.();
      return true;
    } catch (err) {
      console.error("Upload error:", err);
      setUploadError(err.message || "An error occurred during file upload.");
      setUploadStep(0);
      return false;
    }
  };

  // Handle message send
  const handleSend = async () => {
    if (isStreaming || uploadingFile || transcribing || isRecording) return;
    
    let currentInput = input;
    setInput("");
    
    let hasUploaded = true;
    if (attachedFile) {
      hasUploaded = await uploadFile(attachedFile);
      if (!hasUploaded) return; // Halt sending if upload failed
    }

    if (!currentInput.trim() && !attachedFile) return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: currentInput }]);
    setIsStreaming(true);
    setCurrentStreamText("");
    setStreamCitations([]);

    let accumulatedText = "";
    let accumulatedCitations = [];
    let accumulatedLanguage = "English";

    // SSE Streaming
    const url = `${API_BASE}/api/stream?query=${encodeURIComponent(currentInput)}&session_id=${sessionId}${
      conversationId ? `&conversation_id=${conversationId}` : ""
    }&response_language=${language === "en" ? "English" : "Hindi"}`;
    
    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      if (event.data === "[DONE]") {
        eventSource.close();
        eventSourceRef.current = null;
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: accumulatedText,
            citations: accumulatedCitations,
            response_language: accumulatedLanguage,
          },
        ]);
        setCurrentStreamText("");
        setStreamCitations([]);
        setIsStreaming(false);
        onMessageSent?.();
        return;
      }

      try {
        const data = JSON.parse(event.data);
        if (data.skipped_llm) {
          accumulatedText = data.answer;
          accumulatedCitations = data.citations || [];
          accumulatedLanguage = data.response_language || "English";
          setCurrentStreamText(accumulatedText);
        } else if (data.type === "token") {
          accumulatedText += data.data.token;
          setCurrentStreamText(accumulatedText);
        } else if (data.type === "citation") {
          accumulatedCitations = data.data.citations || [];
          setStreamCitations(accumulatedCitations);
        } else if (data.type === "done") {
          accumulatedLanguage = data.data.response_language || "English";
        } else if (data.type === "error") {
          accumulatedText = `[Error: ${data.data.message}]`;
          setCurrentStreamText(accumulatedText);
        }
      } catch (err) {
        console.error("SSE JSON parse error:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("EventSource error:", err);
      eventSource.close();
      eventSourceRef.current = null;
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: accumulatedText || "Connection interrupted. Please try again.",
          citations: accumulatedCitations,
          response_language: accumulatedLanguage,
        },
      ]);
      setCurrentStreamText("");
      setStreamCitations([]);
      setIsStreaming(false);
    };
  };

  const handleStopStreaming = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
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
      />

      {/* Messages area wrapper */}
      <div 
        ref={messagesContainerRef} 
        onScroll={handleScroll}
        className="flex-1 flex flex-col overflow-hidden"
      >
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
      </div>

      {/* Upload Progress Timeline overlay */}
      {uploadingFile && (
        <div className="px-4 max-w-2xl mx-auto w-full">
          <UploadTimeline step={uploadStep} error={uploadError} language={language} />
        </div>
      )}

      {/* Input bar section */}
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

      {/* Scroll bottom FAB */}
      {showScrollBottom && (
        <button
          onClick={() => scrollToBottom()}
          className="absolute bottom-20 right-8 p-2 rounded-full shadow-lg cursor-pointer border-none bg-purple-600 hover:bg-purple-500 text-white transition hover:scale-105 active:scale-95"
        >
          <ArrowDown size={18} />
        </button>
      )}
    </div>
  );
}
