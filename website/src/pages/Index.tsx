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

const Index = () => {
  const features = [
    {
      icon: <BookOpen className="h-6 w-6" />,
      title: "Read Cheat Sheets",
      description: "Access your cheat sheets instantly with `tref git --read`",
      command: "tref git --read",
    },
    {
      icon: <Edit className="h-6 w-6" />,
      title: "Edit Cheat Sheets",
      description: "Modify existing cheat sheets with `tref curl --edit`",
      command: "tref curl --edit",
    },
    {
      icon: <Plus className="h-6 w-6" />,
      title: "Add New Cheat Sheets",
      description: "Create new references with `tref make --add`",
      command: "tref make --add",
    },
    {
      icon: <X className="h-6 w-6" />,
      title: "Delete Cheat Sheets",
      description: "Remove unwanted cheat sheets with `tref ls --delete`",
      command: "tref ls --delete",
    },
    {
      icon: <RefreshCw className="h-6 w-6" />,
      title: "Reset Cheat Sheets",
      description: "Fetch default cheat sheets from GitHub with `tref --reset`",
      command: "tref --reset",
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: "Editor Integration",
      description: "Uses your $EDITOR or defaults to nano",
      command: "export EDITOR=vim",
    },
  ];

  const examples = [
    {
      title: "Reading a cheat sheet",
      command: "tref git --read",
      output: `
# Git Cheat Sheet

## Basic Commands
- git init: Initialize a new repository
- git clone <url>: Clone a repository
- git add <file>: Stage changes
- git commit -m "message": Commit changes
- git push: Push changes to remote
- git pull: Fetch and merge changes

## Branching
- git branch: List branches
- git branch <name>: Create branch
- git checkout <branch>: Switch branch
- git merge <branch>: Merge branch
      `,
    },
    {
      title: "Adding a new cheat sheet",
      command: "tref docker --add",
      output: `
# Opening editor to add Docker cheat sheet...

# Docker Cheat Sheet successfully added!
- Saved to: ~/.config/tref/docker.json
- Access with: tref docker --read
      `,
    },
    {
      title: "Editing a cheat sheet",
      command: "tref python --edit",
      output: `
# Opening Python cheat sheet in editor...

# Cheat sheet updated successfully!
- Modified: ~/.config/tref/python.json
      `,
    },
    {
      title: "Resetting to defaults",
      command: "tref --reset",
      output: `
# Fetching default cheat sheets from GitHub...

✓ Downloaded: git.json
✓ Downloaded: docker.json
✓ Downloaded: python.json
✓ Downloaded: javascript.json
✓ Downloaded: linux.json

# Default cheat sheets restored!
      `,
    },
  ];

  const downloadLinks = [
    {
      platform: "Linux",
      url: "https://github.com/pavandhadge/tref/releases/download/tref/tref_darwin_amd64",
    },
    {
      platform: "macOS",
      url: "https://github.com/pavandhadge/tref/releases/download/tref/tref_darwin_amd64",
    },
    {
      platform: "Windows",
      url: "https://github.com/pavandhadge/tref/releases/download/tref/tref_darwin_amd64",
    },
  ];

  const benefits = [
    {
      icon: <Server className="h-6 w-6" />,
      title: "Lightweight & Fast",
      description:
        "Built with Go for exceptional performance. Starts instantly and uses minimal system resources.",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Offline First",
      description:
        "All your cheat sheets are stored locally. No internet connection required after initial setup.",
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Developer Friendly",
      description:
        "Integrates with your existing workflow and terminal environment. Customizable to your needs.",
    },
  ];

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      {/* Hero Section */}
      <section className="px-4 py-16 md:py-24 max-w-6xl mx-auto text-center">
        <div className="flex justify-center mb-6">
          <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-4 rounded-lg w-20 h-20 flex items-center justify-center shadow-lg">
            <Terminal className="h-12 w-12 text-white" />
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9]">
          tref
        </h1>
        <p className="text-xl md:text-2xl text-slate-600 mb-8 max-w-3xl mx-auto">
          A lightweight{" "}
          <span className="text-[#8B5CF6] font-semibold">Go-powered</span> CLI
          tool to manage and access your development cheat sheets
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
          <Button
            asChild
            size="lg"
            className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] text-white border-none hover:opacity-90"
          >
            <a
              href="https://github.com/pavandhadge/tref/releases/latest"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Download className="mr-2 h-5 w-5" /> Get tref now
            </a>
          </Button>
          <Button
            asChild
            variant="outline"
            size="lg"
            className="border-[#8B5CF6] text-[#8B5CF6] hover:bg-[#8B5CF6]/10"
          >
            <a
              href="https://github.com/pavandhadge/tref"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github className="mr-2 h-5 w-5" /> View on GitHub
            </a>
          </Button>
        </div>

        <div className="flex justify-center">
          <ArrowDown className="h-8 w-8 text-[#8B5CF6] animate-bounce" />
        </div>
      </section>

      {/* About Section - New section with more information */}
      <section className="py-16 bg-[#FAFAFA]">
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
                className="bg-white p-6 shadow-md hover:shadow-lg transition-shadow border-0"
              >
                <div className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] p-3 rounded-lg w-14 h-14 flex items-center justify-center mb-4 text-white">
                  {benefit.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3 text-slate-800">
                  {benefit.title}
                </h3>
                <p className="text-slate-600">{benefit.description}</p>
              </Card>
            ))}
          </div>

          <div className="mt-14 text-center">
            <p className="text-lg md:text-xl text-slate-700 max-w-3xl mx-auto mb-6">
              <span className="font-mono font-bold">tref</span> simplifies your
              development workflow by keeping frequently used commands, snippets
              and references at your fingertips.
            </p>
            <p className="text-slate-600 max-w-2xl mx-auto">
              Stop searching the web for commands you've used before. Create
              personalized cheat sheets once, access them instantly whenever you
              need them, right from your terminal.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 bg-[	#FFFFFF] ">
        {/* <div className="max-w-6xl mx-auto px-4"> */}
        {/* <TerminalHeader command="tref" flag="--features" /> */}
        <div className="max-w-6xl mx-auto px-4">
          <div className=" mb-10">
            <h2 className="text-2xl md:text-3xl font-mono font-bold inline-block">
              <span className="text-[#9b87f5]">$</span> tref{" "}
              <span className="text-[#1EAEDB]">--features</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* Examples Section */}
      <section id="examples" className="py-16 bg-[#F8F8FF]">
        <div className="max-w-6xl mx-auto px-4">
          <div className=" mb-10">
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

      {/* Download Section */}
      <section id="download" className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <div className=" mb-10">
            <h2 className="text-2xl md:text-3xl font-mono font-bold inline-block">
              <span className="text-[#9b87f5]">$</span> tref{" "}
              <span className="text-[#1EAEDB]">--download</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            {downloadLinks.map((link, index) => (
              <Card
                key={index}
                className={cn(
                  "bg-white border-slate-200 hover:border-[#8B5CF6] transition-colors",
                  "flex flex-col items-center justify-center p-6 text-center shadow-md",
                )}
              >
                <h3 className="text-xl font-semibold mb-3 text-slate-800">
                  {link.platform}
                </h3>
                <Button
                  asChild
                  className="bg-gradient-to-r from-[#8B5CF6] to-[#0EA5E9] text-white hover:opacity-90"
                >
                  <a href={link.url} target="_blank" rel="noopener noreferrer">
                    <Download className="mr-2 h-4 w-4" /> Download
                  </a>
                </Button>
              </Card>
            ))}
          </div>

          <div className="mt-12 text-center">
            <p className="text-slate-600 mb-4">
              Alternatively, install with Go:
            </p>
            <div className="bg-slate-800 text-white border border-slate-700 p-4 rounded-lg inline-block font-mono text-sm md:text-base shadow-md">
              <code>$ go install github.com/pavandhadge/tref@latest</code>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Index;
