"use client";

import { useState } from "react";

export default function QueryPanel({
  onAsk,
  loading,
}: {
  onAsk: (q: string) => void;
  loading: boolean;
}) {
  const [query, setQuery] = useState("");

  const canAsk = query.trim().length > 0 && !loading;

  return (
    <div className="border p-4 rounded space-y-2">
      <h2 className="font-semibold">Ask a Question</h2>

      <input
        className="w-full p-2 bg-black border rounded"
        placeholder="What is RAG?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button
        onClick={() => onAsk(query)}
        disabled={!canAsk}
        className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        Ask
      </button>

    </div>
  );
}
