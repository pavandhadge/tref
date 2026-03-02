import React, { useState } from "react";
import Markdown from "react-markdown";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const docFiles = [
  { label: "Interface", file: "/docs/interface.md" },
  { label: "Architecture", file: "/docs/architecture.md" },
  { label: "Tools", file: "/docs/tools.md" },
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
      <main className="mx-auto w-full max-w-7xl px-4 py-12 md:px-6 md:py-14">
        <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white via-slate-50 to-sky-50/60 p-6 shadow-sm md:p-8">
          <div className="inline-flex items-center rounded-full border border-sky-200 bg-white px-3 py-1 text-xs font-semibold tracking-wide text-sky-700">
            tref docs
          </div>
          <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-slate-900 md:text-4xl">Documentation</h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-700 md:text-base">
            Current interface, architecture, tooling, and operational guidance for running tref reliably in local and CI
            environments.
          </p>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
          <aside className="h-fit rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:sticky lg:top-24">
            <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Sections</div>
            <div className="space-y-2">
              {docFiles.map((doc, i) => (
                <button
                  key={doc.label}
                  className={`w-full rounded-xl border px-3 py-2.5 text-left text-sm font-medium transition-colors ${
                    i === tab
                      ? "border-sky-300 bg-sky-50 text-sky-800"
                      : "border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50"
                  }`}
                  onClick={() => setTab(i)}
                >
                  {doc.label}
                </button>
              ))}
            </div>
            <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs leading-5 text-slate-600">
              Tip: use <span className="font-mono text-slate-800">tref config show</span> to inspect effective defaults.
            </div>
          </aside>

          <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            {loading && <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">Loading documentation...</div>}
            {error && <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
            {!loading && !error && typeof content === "string" && (
              <Markdown
                components={{
                  h1: ({ children }) => <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">{children}</h1>,
                  h2: ({ children }) => (
                    <h2 className="mt-10 border-t border-slate-200 pt-6 text-2xl font-semibold tracking-tight text-slate-900">
                      {children}
                    </h2>
                  ),
                  h3: ({ children }) => <h3 className="mt-7 text-xl font-semibold text-slate-900">{children}</h3>,
                  p: ({ children }) => <p className="mt-4 text-[15px] leading-7 text-slate-700">{children}</p>,
                  ul: ({ children }) => <ul className="mt-4 list-disc space-y-2 pl-6 text-[15px] leading-7 text-slate-700">{children}</ul>,
                  ol: ({ children }) => <ol className="mt-4 list-decimal space-y-2 pl-6 text-[15px] leading-7 text-slate-700">{children}</ol>,
                  li: ({ children }) => <li>{children}</li>,
                  code: ({ inline, children }) =>
                    inline ? (
                      <code className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-[0.9em] text-slate-800">{children}</code>
                    ) : (
                      <code className="block overflow-x-auto rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-sm text-slate-100">
                        {children}
                      </code>
                    ),
                  pre: ({ children }) => <pre className="mt-5 overflow-x-auto">{children}</pre>,
                  blockquote: ({ children }) => (
                    <blockquote className="mt-5 border-l-4 border-sky-200 bg-sky-50/60 px-4 py-3 text-slate-700">{children}</blockquote>
                  ),
                  hr: () => <hr className="my-8 border-slate-200" />,
                }}
              >
                {content}
              </Markdown>
            )}
          </article>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Docs;
