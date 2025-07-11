import {
  Terminal,
  ArrowDown,
  Github,
  Code,
  BookOpen,
  Download,
  Plus,
  Edit,
  RefreshCw,
  X,
  Server,
  Shield,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import FeatureCard from "@/components/FeatureCard";
import TerminalDemo from "@/components/TerminalDemo";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import TerminalHeader from "@/components/TerminalHeader";
import { Link } from "react-router-dom";

const Index = () => {
  const features = [
    {
      icon: <BookOpen className="h-6 w-6" />,
      title: "Read Cheat Sheets",
      description: "View your cheat sheets instantly with `--read TOOL`.",
      command: "python3 -m tref.cli --read TOOL",
    },
    {
      icon: <Edit className="h-6 w-6" />,
      title: "Edit Cheat Sheets",
      description: "Modify existing cheat sheets with `--edit TOOL`.",
      command: "python3 -m tref.cli --edit TOOL",
    },
    {
      icon: <Plus className="h-6 w-6" />,
      title: "Add New Cheat Sheets",
      description: "Create new references with `--add TOOL`.",
      command: "python3 -m tref.cli --add TOOL",
    },
    {
      icon: <X className="h-6 w-6" />,
      title: "Delete Cheat Sheets",
      description: "Remove unwanted cheat sheets with `--delete TOOL`.",
      command: "python3 -m tref.cli --delete TOOL",
    },
    {
      icon: <RefreshCw className="h-6 w-6" />,
      title: "Update Embeddings",
      description: "Regenerate semantic search embeddings with `--update-embeddings` after editing sheets.",
      command: "python3 -m tref.cli --update-embeddings",
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: "Semantic Search",
      description: "Find commands by meaning with `--search TOOL QUERY` or use `--interactive` mode.",
      command: "python3 -m tref.cli --search TOOL QUERY",
    },
  ];

  const examples = [
    {
      title: "Reading a cheat sheet",
      command: "python3 -m tref.cli --read git",
      output: `
=== Cheat Sheet for git ===
{
  "git Cheatsheet": {
    "General": [
      {
        "name": "Clone a repository",
        "command": "git clone <url>",
        "explanation": "Clone a remote repository",
        "tags": []
      }
    ]
  }
}
    `,
    },
    {
      title: "Adding a new cheat sheet",
      command: "python3 -m tref.cli --add docker",
      output: `
Created new cheat sheet for 'docker' at ~/.config/tref/cheatsheets/docker.json
# Editor opens for you to add content
    `,
    },
    {
      title: "Semantic search",
      command: "python3 -m tref.cli --search git 'clone repository'",
      output: `
Top results for 'clone repository':

1. Clone a repository (Score: 0.999)
   Command: git clone <url>
   Explanation: Clone a remote repository
    `,
    },
    {
      title: "Interactive search",
      command: "python3 -m tref.cli --interactive",
      output: `
Available tools: git, docker, ...
Enter tool name (or 'quit'): git
Enter your query: clone

Top results:
1. Clone a repository (Score: 0.999)
   Command: git clone <url>
   Explanation: Clone a remote repository
    `,
    },
  ];

  const benefits = [
    {
      icon: <Server className="h-6 w-6" />,
      title: "Fast & Local",
      description:
        "Runs locally with Python and HuggingFace Transformers. No internet required after setup.",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Private & Secure",
      description:
        "Your cheat sheets and embeddings are stored on your machine only.",
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Semantic Search",
      description:
        "Find commands by meaning, not just keywords, using state-of-the-art embeddings.",
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      {/* Hero Section */}
      <section className="relative overflow-hidden w-full px-0 py-20 md:py-32 text-center flex flex-col items-center justify-center min-h-[100vh]">
        {/* Animated background gradient blob */}
        <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[120vw] h-[500px] bg-gradient-to-tr from-[#8B5CF6]/60 via-[#0EA5E9]/40 to-[#8B5CF6]/30 blur-3xl opacity-70 animate-pulse z-0" />
        {/* Floating shapes */}
        <div className="absolute top-10 left-10 w-24 h-24 bg-[#8B5CF6]/30 rounded-full blur-2xl animate-float-slow z-0" />
        <div className="absolute bottom-10 right-10 w-32 h-32 bg-[#0EA5E9]/20 rounded-full blur-2xl animate-float-fast z-0" />
        <div className="relative z-10 flex flex-col items-center w-full">
          <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-6 rounded-2xl w-28 h-28 flex items-center justify-center shadow-2xl border-4 border-white/20 mb-6 animate-bounce-slow">
            <Terminal className="h-16 w-16 text-white drop-shadow-lg" />
          </div>
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] drop-shadow-xl tracking-tight">
            tref
          </h1>
          <p className="text-2xl md:text-3xl text-[#8B5CF6] font-mono font-semibold mb-2 animate-fade-in">
            Terminal cheat sheets, reimagined.
          </p>
          <p className="text-lg md:text-xl text-slate-700 mb-8 max-w-xl mx-auto animate-fade-in delay-200">
            Find, recall, and use your favorite commands in seconds. No more context switching. No more lost snippets.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12 animate-fade-in delay-300">
            <Button
              asChild
              size="lg"
              className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] text-white border-none hover:opacity-90 shadow-lg shadow-[#8B5CF6]/20"
            >
              <a
                href="https://github.com/pavandhadge/tref"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="mr-2 h-5 w-5" /> View on GitHub
              </a>
            </Button>
            <Button
              asChild
              variant="outline"
              size="lg"
              className="border-[#8B5CF6] text-[#8B5CF6] hover:bg-[#8B5CF6]/10 shadow"
            >
              <Link to="/docs">
                📖 Read Documentation
              </Link>
            </Button>
          </div>
          <div className="flex justify-center animate-bounce mt-2">
            <ArrowDown className="h-10 w-10 text-[#8B5CF6]" />
          </div>
        </div>
      </section>

      {/* About Section - New section with more information */}
      <section className="w-full py-20 bg-gradient-to-br from-[#FAFAFA] via-[#F8F8FF] to-[#e9e6fa] border-t border-[#8B5CF6]/10">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-slate-800 mb-10">
            Why{" "}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9]">
              tref
            </span>
            ?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <Card
                key={index}
                className="bg-white/90 p-6 shadow-xl hover:shadow-2xl transition-shadow border-0 backdrop-blur-md"
              >
                <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-3 rounded-lg w-14 h-14 flex items-center justify-center mb-4 text-white shadow-md">
                  {benefit.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-slate-800">
                  {benefit.title}
                </h3>
                <p className="text-slate-600 text-base leading-relaxed">
                  {benefit.description}
                </p>
              </Card>
            ))}
          </div>
          <div className="mt-12 text-center">
            <p className="text-lg md:text-xl text-slate-700 max-w-2xl mx-auto mb-4 font-mono font-semibold">
              Fast. Local. Private. Always at your fingertips.
            </p>
            <p className="text-slate-500 max-w-xl mx-auto text-base">
              tref keeps your knowledge searchable and ready—no internet, no distractions.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="w-full py-20 bg-gradient-to-br from-[#F8F8FF] via-[#e9e6fa] to-[#FAFAFA] border-t border-[#8B5CF6]/10">
        <div className="max-w-6xl mx-auto px-4">
          <div className="mb-8 text-start">
            <h2 className="text-2xl md:text-3xl font-mono font-bold inline-block mb-2">
              <span className="text-[#9b87f5]">$</span> tref{" "}
              <span className="text-[#1EAEDB]">--features</span>
            </h2>
            <p className="text-slate-600 text-base max-w-2xl  mt-2 text-start">
              Everything you need to manage, search, and use your cheat sheets—right from your terminal.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* Examples Section */}
      <section id="examples" className="w-full py-20 bg-gradient-to-br from-[#e9e6fa] via-[#F8F8FF] to-[#FAFAFA] border-t border-[#8B5CF6]/10">
        <div className="max-w-6xl mx-auto px-4">
          <div className="mb-10">
            <h2 className="text-2xl md:text-3xl font-mono font-bold inline-block">
              <span className="text-[#9b87f5]">$</span> tref{" "}
              <span className="text-[#1EAEDB]">--examples</span>
            </h2>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {examples.map((example, index) => (
              <TerminalDemo
                key={index}
                title={example.title}
                command={example.command}
                output={example.output}
              />
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Index;
