import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface TerminalDemoProps {
  title: string;
  command: string;
  output: string;
}

const TerminalDemo = ({ title, command, output }: TerminalDemoProps) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(command);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500);
  };

  return (
    <Card className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 shadow-lg">
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-4 py-2">
        <span className="text-sm font-medium text-slate-200">{title}</span>
        <div className="flex gap-1.5">
          <span className="h-2.5 w-2.5 rounded-full bg-slate-500" />
          <span className="h-2.5 w-2.5 rounded-full bg-slate-600" />
          <span className="h-2.5 w-2.5 rounded-full bg-slate-700" />
        </div>
      </div>

      <div className="p-4">
        <div className="mb-3 flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900 p-2 font-mono text-xs text-slate-200">
          <span className="text-emerald-300">$</span>
          <code className="flex-1 overflow-x-auto whitespace-nowrap">{command}</code>
          <Button
            variant="ghost"
            size="sm"
            className="h-6 px-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white"
            onClick={handleCopy}
          >
            {isCopied ? "Copied" : "Copy"}
          </Button>
        </div>

        <pre className="overflow-x-auto whitespace-pre-wrap rounded-lg border border-slate-800 bg-slate-900 p-4 font-mono text-xs leading-6 text-slate-300">
          {output}
        </pre>
      </div>
    </Card>
  );
};

export default TerminalDemo;
