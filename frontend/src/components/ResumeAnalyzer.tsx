import { useState, useRef } from 'react';
import { FileText, CheckCircle, AlertCircle, XCircle, TrendingUp, Target, Award, Brain, Zap, Eye, FileCheck, AlertTriangle, Upload, X, Loader2, Sparkles } from 'lucide-react';

export function ResumeAnalyzer() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [aiResult, setAiResult] = useState<any>(null); // ⭐ store backend response
  const fileInputRef = useRef<HTMLInputElement>(null);

  // ⭐⭐⭐ REAL BACKEND CONNECTION ⭐⭐⭐
  const processResume = async (file: File) => {
    try {
      setIsProcessing(true);
      setIsAnalyzed(false);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      console.log("AI RESULT:", data);

      setAiResult(data); // save result
      setIsProcessing(false);
      setIsAnalyzed(true);

    } catch (error) {
      console.error("Upload failed:", error);
      alert("Backend not reachable. Make sure FastAPI is running.");
      setIsProcessing(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      processResume(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const file = e.dataTransfer.files[0];
    if (file) {
      setUploadedFile(file);
      processResume(file);
    }
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    setIsProcessing(false);
    setIsAnalyzed(false);
    setAiResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleBrowse = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">

      {/* Upload Section */}
      {!uploadedFile && (
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h2 className="text-xl mb-4">Upload Resume</h2>

          <div
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer"
            onClick={handleBrowse}
          >
            <Upload className="w-10 h-10 mx-auto mb-4 text-purple-600" />
            <p>Click or Drop resume (PDF/DOCX)</p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      )}

      {/* Processing */}
      {uploadedFile && !isAnalyzed && (
        <div className="bg-white p-6 rounded-xl">
          <p>Analyzing: {uploadedFile.name}</p>
          {isProcessing && <Loader2 className="animate-spin mt-4" />}
        </div>
      )}

      {/* ⭐ REAL RESULT DISPLAY ⭐ */}
      {isAnalyzed && aiResult && (
        <div className="bg-white p-6 rounded-xl space-y-4">

          <h2 className="text-2xl">Predicted Role: {aiResult.role}</h2>
          <p>Confidence: {aiResult.confidence}%</p>

          <div>
            <h3 className="font-bold">Detected Skills</h3>
            <ul>
              {aiResult.detected_skills.map((s: string, i: number) => (
                <li key={i}>• {s}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-bold">Missing Skills</h3>
            <ul>
              {aiResult.missing_skills.map((s: string, i: number) => (
                <li key={i}>• {s}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-bold">Roadmap</h3>
            <ul>
              {aiResult.roadmap.map((s: string, i: number) => (
                <li key={i}>→ {s}</li>
              ))}
            </ul>
          </div>

          <button
            onClick={handleRemoveFile}
            className="mt-4 bg-purple-600 text-white px-4 py-2 rounded"
          >
            Analyze Another Resume
          </button>

        </div>
      )}

    </div>
  );
}
