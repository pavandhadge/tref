
import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

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
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <Card className="bg-[hsl(var(--terminal-bg))] border-[#9b87f5]/30 overflow-hidden shadow-md">
      <div className="bg-[hsl(var(--terminal-header))] px-4 py-2 flex justify-between items-center border-b border-[#9b87f5]/20">
        <span className="font-semibold text-sm text-gray-300">{title}</span>
        <div className="flex space-x-1">
          <div className="h-2.5 w-2.5 rounded-full bg-red-500"></div>
          <div className="h-2.5 w-2.5 rounded-full bg-yellow-500"></div>
          <div className="h-2.5 w-2.5 rounded-full bg-green-500"></div>
        </div>
      </div>
      
      <div className="p-4">
        <div className="flex items-center gap-2 mb-3 font-mono">
          <span className="text-[#9b87f5]">$</span>
          <div className="flex-1 bg-[hsl(var(--terminal-header))] p-2 rounded flex items-center justify-between">
            <code className="text-sm text-gray-300">{command}</code>
            <Button 
              variant="ghost" 
              size="sm" 
              className="h-6 text-xs hover:bg-[#9b87f5]/10 hover:text-[#9b87f5] text-gray-300"
              onClick={handleCopy}
            >
              {isCopied ? "Copied!" : "Copy"}
            </Button>
          </div>
        </div>
        
        <div className="bg-[hsl(var(--terminal-header))] p-4 rounded font-mono text-sm overflow-x-auto whitespace-pre-wrap">
          <pre className="text-gray-300">{output}</pre>
        </div>
      </div>
    </Card>
  );
};

export default TerminalDemo;
