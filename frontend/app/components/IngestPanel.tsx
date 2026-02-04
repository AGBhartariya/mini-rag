"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

export default function IngestPanel() {
  const [text, setText] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<"paste" | "file">("paste");

  // -----------------------------
  // TEXT INGEST
  // -----------------------------
  async function handleTextIngest() {
    if (!API_BASE) {
      setStatus("❌ NEXT_PUBLIC_API_BASE is not configured");
      return;
    }

    if (!text.trim()) {
      setStatus("❌ Please paste a document first.");
      return;
    }

    try {
      setLoading(true);
      setStatus("⏳ Ingesting document…");

      const res = await fetch(`${API_BASE}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_text: text,
          title: "Uploaded Text",
        }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || "Ingest failed");
      }

      setStatus("✅ Your document has been ingested successfully");
      setText("");
    } catch (err) {
      console.error(err);
      setStatus("❌ Failed to ingest document");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------
  // PDF INGEST
  // -----------------------------
  async function handlePdfUpload(file: File) {
    if (!API_BASE) {
      setStatus("❌ NEXT_PUBLIC_API_BASE is not configured");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setStatus("❌ Only PDF files are supported");
      return;
    }

    try {
      setLoading(true);
      setStatus("⏳ Uploading and processing PDF…");

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/ingest/pdf`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "PDF ingest failed");
      }

      setStatus("✅ PDF has been ingested successfully");
    } catch (err) {
      console.error(err);
      setStatus("❌ Failed to ingest PDF");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border p-4 rounded space-y-3">
      <h2 className="font-semibold">Ingest Document</h2>

      {/* Mode Toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            setMode("paste");
            setStatus(null);
          }}
          className={`px-3 py-1 rounded border ${
            mode === "paste"
              ? "bg-blue-600 text-white"
              : "bg-black text-gray-400"
          }`}
        >
          Paste Text
        </button>

        <button
          onClick={() => {
            setMode("file");
            setStatus(null);
          }}
          className={`px-3 py-1 rounded border ${
            mode === "file"
              ? "bg-blue-600 text-white"
              : "bg-black text-gray-400"
          }`}
        >
          Upload PDF
        </button>
      </div>

      {/* Paste Mode */}
      {mode === "paste" && (
        <textarea
          className="w-full h-40 border p-2 bg-black rounded"
          placeholder="Paste your document here…"
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            setStatus(null);
          }}
          disabled={loading}
        />
      )}

      {/* PDF Upload Mode */}
      {mode === "file" && (
        <input
          type="file"
          accept="application/pdf"
          disabled={loading}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handlePdfUpload(file);
          }}
          className="text-sm text-gray-400"
        />
      )}

      {/* Ingest Button (only for text mode) */}
      {mode === "paste" && (
        <button
          onClick={handleTextIngest}
          disabled={loading}
          className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Ingesting…" : "Ingest"}
        </button>
      )}

      {/* Status */}
      {status && (
        <div className="text-sm text-gray-400 border border-gray-600/30 rounded p-2">
          {status}
        </div>
      )}
    </div>
  );
}
