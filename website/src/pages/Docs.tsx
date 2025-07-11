import React, { useState } from "react";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import Markdown from "react-markdown";

const docFiles = [
  { label: "Overview & Interface", file: "/docs/interface.md" },
  { label: "Architecture", file: "/docs/architecture.md" },
  { label: "Tools Used", file: "/docs/tools.md" },
];

const Docs = () => {
  const [tab, setTab] = useState(0);
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  React.useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(docFiles[tab].file)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load documentation.");
        return res.text();
      })
      .then((text) => setContent(text))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [tab]);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <section className="px-4 py-16 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">tref Documentation</h1>
        <div className="flex gap-2 mb-6">
          {docFiles.map((doc, i) => (
            <button
              key={doc.label}
              className={`px-4 py-2 rounded-t font-mono border-b-2 ${i === tab ? "border-[#8B5CF6] bg-[#F8F8FF]" : "border-transparent bg-slate-100"}`}
              onClick={() => setTab(i)}
            >
              {doc.label}
            </button>
          ))}
        </div>
        <div className="prose prose-slate max-w-none bg-white p-6 rounded shadow">
          {loading && <div>Loading...</div>}
          {error && <div className="text-red-600">{error}</div>}
          {!loading && !error && typeof content === "string" && (
            <Markdown children={content} />
          )}
        </div>
      </section>
      <Footer />
    </div>
  );
};

export default Docs; 