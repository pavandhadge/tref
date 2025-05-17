import { Github } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-12 bg-[hsl(var(--terminal-bg))] text-[hsl(var(--terminal-text))] border-t border-[#9b87f5]/20">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-6 md:mb-0 text-center md:text-left">
            <div className="text-2xl font-mono font-bold text-[#9b87f5] mb-2">
              tref
            </div>
            <p className="text-gray-300">Terminal Reference Tool</p>
          </div>

          <div className="flex flex-col items-center md:items-end">
            <p className="text-gray-300 mb-2">Built by Pavan Dhadge</p>
            <a
              href="https://github.com/pavandhadge"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center text-[#9b87f5] hover:underline"
            >
              <Github className="h-4 w-4 mr-1" /> @pavandhadge
            </a>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-[#9b87f5]/20 text-center text-sm text-gray-400">
          <p>tref is open source and available under the AGPL3 license.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
