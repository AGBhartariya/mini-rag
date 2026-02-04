
// // "use client";

// // import SourceCard from "./SourceCard";

// // type CostEstimate = {
// //   input_tokens: number;
// //   output_tokens: number;
// //   approx_cost_usd: number;
// // };

// // export default function AnswerPanel({
// //   answer,
// //   sources,
// //   timings,
// //   loading,
// //   error,
// //   costEstimate,
// // }: {
// //   answer: string | null;
// //   sources: any[];
// //   timings: {
// //     retrieval_ms: number;
// //     generation_ms: number;
// //   } | null;
// //   loading: boolean;
// //   error: string | null;
// //   costEstimate?: CostEstimate | null;
// // }) {
// //   // ---------------------------
// //   // Error state
// //   // ---------------------------
// //   if (error) {
// //     return (
// //       <div className="p-4 border border-red-600 bg-red-900/20 text-red-300 rounded">
// //         {error}
// //       </div>
// //     );
// //   }

// //   // ---------------------------
// //   // Loading state
// //   // ---------------------------
// //   if (loading) {
// //     return (
// //       <section className="border p-4 rounded space-y-2">
// //         <h2 className="font-semibold">Answer</h2>
// //         <p className="text-sm text-gray-400">Thinking…</p>
// //       </section>
// //     );
// //   }

// //   // ---------------------------
// //   // Empty state
// //   // ---------------------------
// //   if (!answer) {
// //     return (
// //       <section className="border p-4 rounded text-gray-500 italic">
// //         Ask a question to see grounded answers with citations.
// //       </section>
// //     );
// //   }

// //   // ---------------------------
// //   // Normal state
// //   // ---------------------------
// //   return (
// //     <section className="border p-4 rounded space-y-4">
// //       <div className="flex items-center justify-between">
// //         <h2 className="font-semibold">Answer</h2>
// //         <span className="px-2 py-1 text-xs rounded bg-blue-800/40 text-blue-300">
// //           RAG · Grounded
// //         </span>
// //       </div>

// //       <div className="prose prose-invert max-w-none text-lg leading-relaxed">
// //         {answer}
// //       </div>

// //       {timings && (
// //         <div className="text-xs text-gray-400">
// //           Retrieval: {timings.retrieval_ms} ms · Generation:{" "}
// //           {timings.generation_ms} ms
// //         </div>
// //       )}

// //       {costEstimate && (
// //         <div className="text-xs text-gray-400">
// //           Tokens: {costEstimate.input_tokens} in /{" "}
// //           {costEstimate.output_tokens} out ·
// //           Cost ≈ ${costEstimate.approx_cost_usd}
// //         </div>
// //       )}

// //       {sources.length > 0 && (
// //         <>
// //           <h3 className="font-semibold mt-4">Sources</h3>
// //           <div className="space-y-2">
// //             {sources.map((s) => (
// //               <SourceCard key={s.id} source={s} />
// //             ))}
// //           </div>
// //         </>
// //       )}
// //     </section>
// //   );
// // }


// "use client";

// import SourceCard from "./SourceCard";

// /* -----------------------------
//  Types
// ----------------------------- */

// type Citation = {
//   citation_id: number;
//   chunk_id: string;
// };

// type AnswerPayload = {
//   text: string;
//   citations: Citation[];
// };

// type CostEstimate = {
//   input_tokens: number;
//   output_tokens: number;
//   approx_cost_usd: number;
// };

// /* -----------------------------
//  Component
// ----------------------------- */

// export default function AnswerPanel({
//   answer,
//   sources,
//   timings,
//   loading,
//   error,
//   costEstimate,
// }: {
//   answer: AnswerPayload | null;
//   sources: any[];
//   timings: {
//     retrieval_ms: number;
//     generation_ms: number;
//   } | null;
//   loading: boolean;
//   error: string | null;
//   costEstimate?: CostEstimate | null;
// }) {
//   /* ---------------------------
//      Error state
//   --------------------------- */
//   if (error) {
//     return (
//       <div className="p-4 border border-red-600 bg-red-900/20 text-red-300 rounded">
//         {error}
//       </div>
//     );
//   }

//   /* ---------------------------
//      Loading state
//   --------------------------- */
//   if (loading) {
//     return (
//       <section className="border p-4 rounded space-y-2">
//         <h2 className="font-semibold">Answer</h2>
//         <p className="text-sm text-gray-400">Thinking…</p>
//       </section>
//     );
//   }

//   /* ---------------------------
//      Empty state
//   --------------------------- */
//   if (!answer) {
//     return (
//       <section className="border p-4 rounded text-gray-500 italic">
//         Ask a question to see grounded answers with citations.
//       </section>
//     );
//   }

//   /* ---------------------------
//      Normal state
//   --------------------------- */
//   return (
//     <section className="border p-4 rounded space-y-4">
//       {/* Header */}
//       <div className="flex items-center justify-between">
//         <h2 className="font-semibold">Answer</h2>
//         <span className="px-2 py-1 text-xs rounded bg-blue-800/40 text-blue-300">
//           RAG · Grounded
//         </span>
//       </div>

//       {/* Answer text */}
//       {/* <div className="prose prose-invert max-w-none text-lg leading-relaxed">
//         {answer.text}
//       </div> */}

//       <div
//         className="prose prose-invert max-w-none text-lg"
//         dangerouslySetInnerHTML={{
//             __html: answer.replace(
//             /\[(\d+)\]/g,
//             `<a href="#source-$1" class="text-blue-400 hover:underline">[$1]</a>`
//             ),
//         }}
//       />


//       {/* Explicit citation mapping (VERY IMPORTANT FOR EVAL) */}
//       {answer.citations.length > 0 && (
//         <div className="text-sm text-blue-400">
//           Citations used:&nbsp;
//           {answer.citations.map((c) => (
//             <span key={c.citation_id} className="mr-2">
//               [{c.citation_id} → chunk {c.chunk_id}]
//             </span>
//           ))}
//         </div>
//       )}

//       {/* Timings */}
//       {timings && (
//         <div className="text-xs text-gray-400">
//           Retrieval: {timings.retrieval_ms} ms · Generation:{" "}
//           {timings.generation_ms} ms
//         </div>
//       )}

//       {/* Cost */}
//       {costEstimate && (
//         <div className="text-xs text-gray-400">
//           Tokens: {costEstimate.input_tokens} in /{" "}
//           {costEstimate.output_tokens} out · Cost ≈ $
//           {costEstimate.approx_cost_usd}
//         </div>
//       )}

//       {/* Sources */}
//       {sources.length > 0 && (
//         <>
//           <h3 className="font-semibold mt-4">Sources</h3>
//           <div className="space-y-2">
//             {sources.map((s) => (
//               <SourceCard key={s.id} source={s} />
//             ))}
//           </div>
//         </>
//       )}
//     </section>
//   );
// }

"use client";

import SourceCard from "./SourceCard";

/* -----------------------------
 Types
----------------------------- */

type Citation = {
  citation_id: number;
  chunk_id: string;
};

type AnswerPayload = {
  text: string;
  citations: Citation[];
};

type CostEstimate = {
  input_tokens: number;
  output_tokens: number;
  approx_cost_usd: number;
};

/* -----------------------------
 Component
----------------------------- */

export default function AnswerPanel({
  answer,
  sources,
  timings,
  loading,
  error,
  costEstimate,
}: {
  answer: AnswerPayload | null;
  sources: any[];
  timings: {
    retrieval_ms: number;
    generation_ms: number;
  } | null;
  loading: boolean;
  error: string | null;
  costEstimate?: CostEstimate | null;
}) {
  /* ---------------------------
     Error state
  --------------------------- */
  if (error) {
    return (
      <div className="p-4 border border-red-600 bg-red-900/20 text-red-300 rounded">
        {error}
      </div>
    );
  }

  /* ---------------------------
     Loading state
  --------------------------- */
  if (loading) {
    return (
      <section className="border p-4 rounded space-y-2">
        <h2 className="font-semibold">Answer</h2>
        <p className="text-sm text-gray-400">Thinking…</p>
      </section>
    );
  }

  /* ---------------------------
     Empty state
  --------------------------- */
  if (!answer) {
    return (
      <section className="border p-4 rounded text-gray-500 italic">
        Ask a question to see grounded answers with citations.
      </section>
    );
  }

  /* ---------------------------
     Normal state
  --------------------------- */
  return (
    <section className="border p-4 rounded space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="font-semibold">Answer</h2>
        <span className="px-2 py-1 text-xs rounded bg-blue-800/40 text-blue-300">
          RAG · Grounded
        </span>
      </div>

      {/* Answer text with clickable citations */}
      <div
        className="prose prose-invert max-w-none text-lg leading-relaxed"
        dangerouslySetInnerHTML={{
          __html: answer.text.replace(
            /\[(\d+)\]/g,
            `<a href="#source-$1" class="text-blue-400 hover:underline">[$1]</a>`
          ),
        }}
      />

      {/* Explicit citation mapping (IMPORTANT FOR EVAL) */}
      {answer.citations.length > 0 && (
        <div className="text-sm text-blue-400">
          Citations used:&nbsp;
          {answer.citations.map((c) => (
            <span key={c.citation_id} className="mr-2">
              [{c.citation_id} → chunk {c.chunk_id}]
            </span>
          ))}
        </div>
      )}

      {/* Timings */}
      {timings && (
        <div className="text-xs text-gray-400">
          Retrieval: {timings.retrieval_ms} ms · Generation:{" "}
          {timings.generation_ms} ms
        </div>
      )}

      {/* Cost */}
      {costEstimate && (
        <div className="text-xs text-gray-400">
          Tokens: {costEstimate.input_tokens} in /{" "}
          {costEstimate.output_tokens} out · Cost ≈ $
          {costEstimate.approx_cost_usd}
        </div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <>
          <h3 className="font-semibold mt-4">Sources</h3>
          <div className="space-y-2">
            {sources.map((s) => (
              <SourceCard key={s.id} source={s} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
