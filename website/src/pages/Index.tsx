import { ArrowRight, BookOpen, CheckCircle2, Code2, Download, Github, ShieldCheck, Sparkles, Terminal, Zap } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import FeatureCard from "@/components/FeatureCard";
import TerminalDemo from "@/components/TerminalDemo";
import Footer from "@/components/Footer";
import Header from "@/components/Header";

const Index = () => {
  const features = [
    {
      icon: <BookOpen className="h-5 w-5" />,
      title: "Versioned Retrieval",
      description: "Ask against exact snapshots like pandas@2.2, git@2.44, docker@26.1 with deterministic context.",
      command: 'tref "pandas@2.2 groupby multiple columns agg mean"',
    },
    {
      icon: <Code2 className="h-5 w-5" />,
      title: "Structured Output",
      description: "Each answer is organized into description, signature, cautions, examples, references, and alternatives.",
      command: 'tref "git@2.44 create a new branch and switch"',
    },
    {
      icon: <Sparkles className="h-5 w-5" />,
      title: "Live Session Mode",
      description: "Stay in an always-on terminal session and keep asking continuously with inline query flags.",
      command: "tref live",
    },
    {
      icon: <ShieldCheck className="h-5 w-5" />,
      title: "Trust-Aware Updates",
      description: "Checksum verification by default with optional signature requirements and freshness/trust notices.",
      command: "tref update --strict-verify",
    },
    {
      icon: <Zap className="h-5 w-5" />,
      title: "Language-Aware Examples",
      description: "Prefer examples by language for mixed stacks without changing query intent.",
      command: 'tref --lang bash "git@2.44 create branch"',
    },
    {
      icon: <CheckCircle2 className="h-5 w-5" />,
      title: "Quality Gates",
      description: "Run golden-query regression checks locally or in CI before shipping snapshot updates.",
      command: "tref eval --index-root /tmp/tref-indexes --min-pass-rate 1.0",
    },
  ];

  const examples = [
    {
      title: "Version mapping + structured guidance",
      command: 'tref "pandas@2.2.0 groupby"',
      output: `pandas@2.2 • DataFrame.groupby
Version Notice: Requested '2.2.0', using '2.2' (compatible-normalized).

Description
Signature
Parameters
Gotchas & Version Notes
Examples
References`,
    },
    {
      title: "Inline flags in live mode",
      command: 'git@2.44 create a new branch and switch --lang bash --top-k 8',
      output: `Examples
Example 1
Language  bash
\`\`\`
git switch -c feature/login-flow
\`\`\`

Other Good Options
• git checkout -b <name>`,
    },
    {
      title: "Trust and freshness status",
      command: "tref status",
      output: `{
  "freshness": {
    "fresh": false,
    "trusted": false,
    "verified": false,
    "verified_signature": false,
    "sla_met": false
  }
}`,
    },
    {
      title: "Regression quality gate",
      command: "tref eval --index-root /tmp/tref-indexes --min-pass-rate 1.0",
      output: `{
  "total": 7,
  "passed": 7,
  "failed": 0,
  "pass_rate": 1.0,
  "min_pass_rate": 1.0
}`,
    },
  ];

  const pillars = [
    "Offline after first successful index sync",
    "Strict schema for KB authoring (LLM-friendly)",
    "Remote endpoints configurable by user",
    "Cross-platform defaults via config file",
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      <main>
        <section className="relative overflow-hidden border-b border-slate-200">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_25%_0%,rgba(14,165,233,0.18),transparent_36%),radial-gradient(circle_at_80%_10%,rgba(20,184,166,0.16),transparent_40%)]" />
          <div className="relative mx-auto max-w-6xl px-4 pb-20 pt-16 md:pb-24 md:pt-24">
            <div className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white/80 px-3 py-1 text-xs font-medium text-slate-700">
              <Terminal className="h-3.5 w-3.5" />
              Production-ready CLI reference engine
            </div>

            <h1 className="mt-6 max-w-4xl text-balance text-4xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-6xl">
              tref makes versioned developer docs queryable like a real tool, not a notes file.
            </h1>

            <p className="mt-6 max-w-2xl text-pretty text-lg leading-8 text-slate-600">
              Ask natural language questions with <span className="font-mono">library@version</span>, get grounded responses, and keep everything local-first with trust-aware updates.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg" className="rounded-xl bg-slate-900 px-6 text-white hover:bg-slate-800">
                <a href="https://github.com/pavandhadge/tref" target="_blank" rel="noopener noreferrer">
                  <Github className="mr-2 h-4 w-4" />
                  View Repository
                </a>
              </Button>
              <Button asChild size="lg" variant="outline" className="rounded-xl border-slate-300 px-6 text-slate-800">
                <a href="https://github.com/pavandhadge/tref/releases" target="_blank" rel="noopener noreferrer">
                  <Download className="mr-2 h-4 w-4" />
                  Download Release
                </a>
              </Button>
              <Button asChild size="lg" variant="ghost" className="rounded-xl text-slate-700 hover:bg-white/70">
                <Link to="/docs">
                  Read Docs <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>

            <div className="mt-10 grid gap-3 sm:grid-cols-2">
              {pillars.map((item) => (
                <div key={item} className="rounded-xl border border-slate-200 bg-white/70 px-4 py-3 text-sm text-slate-700 backdrop-blur">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="features" className="mx-auto w-full max-w-6xl px-4 py-16 md:py-20">
          <div className="mb-8">
            <p className="font-mono text-sm font-medium text-sky-700">Capabilities</p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">Everything needed for reliable local retrieval</h2>
          </div>

          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <FeatureCard key={feature.title} {...feature} />
            ))}
          </div>
        </section>

        <section id="examples" className="border-y border-slate-200 bg-slate-50/70">
          <div className="mx-auto w-full max-w-6xl px-4 py-16 md:py-20">
            <div className="mb-8">
              <p className="font-mono text-sm font-medium text-teal-700">Examples</p>
              <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">Terminal flows you can use immediately</h2>
            </div>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {examples.map((example) => (
                <TerminalDemo key={example.title} title={example.title} command={example.command} output={example.output} />
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto w-full max-w-6xl px-4 py-16 md:py-20">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm md:p-10">
            <h3 className="text-2xl font-bold text-slate-900 md:text-3xl">Ready to use tref in your workflow?</h3>
            <p className="mt-3 max-w-2xl text-slate-600">
              Install once, configure defaults once, and run reproducible retrieval in local dev, Docker, and CI.
            </p>
            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              <Button asChild className="rounded-xl bg-slate-900 text-white hover:bg-slate-800">
                <a href="https://github.com/pavandhadge/tref/releases" target="_blank" rel="noopener noreferrer">Get Latest Release</a>
              </Button>
              <Button asChild variant="outline" className="rounded-xl border-slate-300 text-slate-800">
                <Link to="/docs">Open Documentation</Link>
              </Button>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
