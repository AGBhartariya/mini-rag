const BASE = process.env.NEXT_PUBLIC_API_BASE;

export async function ingestDocument(text: string, title?: string) {
  const res = await fetch(`${BASE}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      document_text: text,
      title: title || "Uploaded Document",
    }),
  });

  if (!res.ok) {
    throw new Error("Ingest failed");
  }

  return res.json();
}

export async function askQuestion(query: string) {
  const res = await fetch(`${BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error("Ask failed");
  }

  return res.json();
}

