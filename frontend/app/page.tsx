// // "use client";

// // import { useState } from "react";
// // import IngestPanel from "./components/IngestPanel";
// // import QueryPanel from "./components/QueryPanel";
// // import AnswerPanel from "./components/AnswerPanel";

// // export default function Home() {
// //   const [answer, setAnswer] = useState<string | null>(null);
// //   const [sources, setSources] = useState<any[]>([]);
// //   const [timings, setTimings] = useState<any>(null);
// //   const [loading, setLoading] = useState(false);
// //   const [error, setError] = useState<string | null>(null);

// //   async function handleAsk(query: string) {
// //     const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

// //     if (!API_BASE) {
// //       setError("API base URL not configured");
// //       return;
// //     }

// //     try {
// //       setLoading(true);
// //       setError(null);
// //       setAnswer(null);
// //       setSources([]);

// //       const res = await fetch(`${API_BASE}/ask`, {
// //         method: "POST",
// //         headers: { "Content-Type": "application/json" },
// //         body: JSON.stringify({ query }),
// //       });

// //       if (!res.ok) throw new Error("Ask failed");

// //       const data = await res.json();

// //       if (!data.sources || data.sources.length === 0) {
// //         setAnswer("I don’t know — no relevant information was found.");
// //         setSources([]);
// //       } else {
// //         setAnswer(data.answer);
// //         setSources(data.sources);
// //       }

// //       setTimings(data.timings);
// //     } catch (err) {
// //       console.error(err);
// //       setError("Failed to reach backend.");
// //     } finally {
// //       setLoading(false);
// //     }
// //   }

// //   return (
// //     <main className="max-w-3xl mx-auto p-6 space-y-6">
// //       <h1 className="text-2xl font-bold">Mini RAG Demo</h1>

// //       <IngestPanel />

// //       <QueryPanel onAsk={handleAsk} loading={loading} />

// //       <AnswerPanel
// //         answer={answer}
// //         sources={sources}
// //         timings={timings}
// //         error={error} loading={false}      />
// //     </main>
// //   );
// // }

// "use client";

// import { useState } from "react";
// import IngestPanel from "./components/IngestPanel";
// import QueryPanel from "./components/QueryPanel";
// import AnswerPanel from "./components/AnswerPanel";

// const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

// export default function Home() {
//   const [answer, setAnswer] = useState<string | null>(null);
//   const [sources, setSources] = useState<any[]>([]);
//   const [timings, setTimings] = useState<any>(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);

//   async function handleAsk(query: string) {
//     if (!API_BASE) {
//       setError("❌ NEXT_PUBLIC_API_BASE is not configured");
//       return;
//     }

//     try {
//       setLoading(true);
//       setError(null);
//       setAnswer(null);
//       setSources([]);
//       setTimings(null);

//       console.log("Calling:", `${API_BASE}/ask`);

//       const res = await fetch(`${API_BASE}/ask`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ query }),
//       });

//       if (!res.ok) {
//         const text = await res.text();
//         throw new Error(text || "Ask endpoint failed");
//       }

//       const data = await res.json();

//       if (!data.sources || data.sources.length === 0) {
//         setAnswer("I don’t know — no relevant information was found.");
//         setSources([]);
//       } else {
//         setAnswer(data.answer);
//         setSources(data.sources);
//       }

//       setTimings(data.timings);
//     } catch (err: any) {
//       console.error("Ask error:", err);
//       setError("❌ Backend unreachable or /ask failed");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <main className="max-w-3xl mx-auto p-6 space-y-6">
//       <h1 className="text-2xl font-bold">Mini RAG Demo</h1>

//       <IngestPanel />

//       <QueryPanel onAsk={handleAsk} loading={loading} />

//       <AnswerPanel
//         answer={answer}
//         sources={sources}
//         timings={timings}
//         error={error}
//         loading={loading}
//       />
//     </main>
//   );
// }

"use client";

import { useState } from "react";
import IngestPanel from "./components/IngestPanel";
import QueryPanel from "./components/QueryPanel";
import AnswerPanel from "./components/AnswerPanel";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

export default function Home() {
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<any[]>([]);
  const [timings, setTimings] = useState<any>(null);
  const [costEstimate, setCostEstimate] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAsk(query: string) {
    if (!API_BASE) {
      setError("❌ NEXT_PUBLIC_API_BASE is not configured");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setAnswer(null);
      setSources([]);
      setTimings(null);
      setCostEstimate(null);

      const res = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Ask endpoint failed");
      }

      const data = await res.json();

      if (!data.sources || data.sources.length === 0) {
        setAnswer("I don’t know — no relevant information was found.");
        setSources([]);
      } else {
        setAnswer(data.answer);
        setSources(data.sources);
      }

      setTimings(data.timings);
      setCostEstimate(data.cost_estimate ?? null);
    } catch (err) {
      console.error("Ask error:", err);
      setError("❌ Backend unreachable or /ask failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-bold">Mini RAG Demo</h1>
        <p className="text-sm text-gray-400">
          Grounded answers with retrieval, reranking, and citations
        </p>
      </header>

      <IngestPanel />

      <QueryPanel onAsk={handleAsk} loading={loading} />

      <AnswerPanel
        answer={answer as any}
        sources={sources}
        timings={timings}
        costEstimate={costEstimate}
        loading={loading}
        error={error}
      />
    </main>
  );
}
