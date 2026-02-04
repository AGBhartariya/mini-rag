// export default function SourceCard({ source }: { source: any }) {
//   return (
//     <div
//       className={`p-3 rounded border transition ${
//         source.used
//           ? "border-green-500 bg-green-900/20"
//           : "border-gray-700 bg-black"
//       }`}
//     >
//       <p className="text-sm whitespace-pre-wrap">{source.text}</p>
//       <p className="text-xs text-gray-400 mt-2">
//         chunk {source.metadata.chunk_id} · chars{" "}
//         {source.metadata.start_char}–{source.metadata.end_char}
//       </p>
//     </div>
//   );
// }

export default function SourceCard({ source }: { source: any }) {
  return (
    <div
      id={`source-${source.id}`}   // ⭐ anchor target
      className={`border rounded p-3 text-sm ${
        source.used
          ? "border-blue-500 bg-blue-900/20"
          : "border-gray-700"
      }`}
    >
      <div className="flex justify-between items-center mb-1">
        <span className="font-mono text-xs text-gray-400">
          Source [{source.id}]
        </span>

        {source.used && (
          <span className="text-xs text-blue-300">
            Used in answer
          </span>
        )}
      </div>

      <pre className="whitespace-pre-wrap text-gray-200">
        {source.text}
      </pre>
    </div>
  );
}

