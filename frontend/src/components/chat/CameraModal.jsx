import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Camera, X, RotateCw, Crop, Check, RefreshCw } from "lucide-react";
import { translations } from "../../utils/localization";

export default function CameraModal({ isOpen, onClose, onCapture, language }) {
  const t = translations[language] || translations.en;
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [rotation, setRotation] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen && !capturedImage) {
      startCamera();
    }
    return () => {
      stopCamera();
    };
  }, [isOpen, capturedImage]);

  const startCamera = async () => {
    setError(null);
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error("Camera access error:", err);
      setError(t.noCameraDetected || "No camera detected.");
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    
    // Set canvas dimensions to match video stream
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const dataUrl = canvas.toDataURL("image/jpeg");
    setCapturedImage(dataUrl);
    stopCamera();
  };

  const rotatePhoto = () => {
    setRotation((prev) => (prev + 90) % 360);
  };

  const handleConfirm = () => {
    if (!canvasRef.current || !capturedImage) return;
    
    // Apply rotation before sending if rotation > 0
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    
    if (rotation !== 0) {
      const tempCanvas = document.createElement("canvas");
      const tempCtx = tempCanvas.getContext("2d");
      
      const angle = (rotation * Math.PI) / 180;
      const width = canvas.width;
      const height = canvas.height;
      
      if (rotation === 90 || rotation === 270) {
        tempCanvas.width = height;
        tempCanvas.height = width;
      } else {
        tempCanvas.width = width;
        tempCanvas.height = height;
      }
      
      tempCtx.translate(tempCanvas.width / 2, tempCanvas.height / 2);
      tempCtx.rotate(angle);
      tempCtx.drawImage(canvas, -width / 2, -height / 2);
      
      tempCanvas.toBlob((blob) => {
        const file = new File([blob], `camera_${Date.now()}.jpg`, { type: "image/jpeg" });
        onCapture(file);
        handleClose();
      }, "image/jpeg", 0.95);
    } else {
      canvas.toBlob((blob) => {
        const file = new File([blob], `camera_${Date.now()}.jpg`, { type: "image/jpeg" });
        onCapture(file);
        handleClose();
      }, "image/jpeg", 0.95);
    }
  };

  const handleRetake = () => {
    setCapturedImage(null);
    setRotation(0);
  };

  const handleClose = () => {
    stopCamera();
    setCapturedImage(null);
    setRotation(0);
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-lg rounded-2xl overflow-hidden glass-strong flex flex-col max-h-[90vh]"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b" style={{ borderColor: "var(--border)" }}>
            <div className="flex items-center gap-2">
              <Camera className="text-purple-500" size={18} />
              <h3 className="text-sm font-bold" style={{ color: "var(--text-primary)" }}>
                {t.cameraTitle}
              </h3>
            </div>
            <button onClick={handleClose} className="btn-ghost p-1 cursor-pointer border-none bg-transparent">
              <X size={18} style={{ color: "var(--text-secondary)" }} />
            </button>
          </div>

          {/* Camera Viewport / Captured Preview */}
          <div className="relative flex-1 bg-black aspect-video flex items-center justify-center min-h-[300px]">
            {error ? (
              <div className="text-center p-6 space-y-3">
                <p className="text-xs text-red-400 font-medium">{error}</p>
                <button onClick={startCamera} className="btn-primary">
                  <RefreshCw size={14} /> Retry
                </button>
              </div>
            ) : !capturedImage ? (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-full object-cover transform scale-x-[-1]"
              />
            ) : (
              <div className="relative w-full h-full flex items-center justify-center overflow-hidden">
                <img
                  src={capturedImage}
                  alt="Captured"
                  className="max-w-full max-h-full object-contain transition-transform duration-300"
                  style={{ transform: `rotate(${rotation}deg)` }}
                />
              </div>
            )}
            
            {/* Hidden canvas used for capture & transform */}
            <canvas ref={canvasRef} className="hidden" />
          </div>

          {/* Actions Bar */}
          <div className="p-4 border-t flex items-center justify-center gap-4 bg-black/40" style={{ borderColor: "var(--border)" }}>
            {!capturedImage ? (
              <button
                onClick={capturePhoto}
                disabled={!!error}
                className="w-12 h-12 rounded-full bg-purple-600 hover:bg-purple-500 text-white flex items-center justify-center cursor-pointer border-none shadow-lg hover:scale-105 active:scale-95 transition"
              >
                <Camera size={20} />
              </button>
            ) : (
              <div className="flex items-center gap-3">
                <button
                  onClick={handleRetake}
                  className="btn-ghost flex items-center gap-1.5 px-4 py-2 cursor-pointer border-none"
                  style={{ color: "var(--text-secondary)" }}
                >
                  <RefreshCw size={14} />
                  {t.retake}
                </button>
                <button
                  onClick={rotatePhoto}
                  className="btn-ghost flex items-center gap-1.5 px-4 py-2 cursor-pointer border-none"
                  style={{ color: "var(--text-secondary)" }}
                >
                  <RotateCw size={14} />
                  {t.rotate}
                </button>
                <button
                  onClick={handleConfirm}
                  className="btn-primary flex items-center gap-1.5 px-5 py-2 cursor-pointer border-none"
                >
                  <Check size={14} />
                  {t.confirm}
                </button>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
