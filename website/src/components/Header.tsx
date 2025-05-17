
import { useState, useEffect } from "react";
import { Terminal, Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY;
      setIsScrolled(scrollTop > 50);
    };
    
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className={cn(
      "sticky top-0 z-10 transition-all duration-300",
      isScrolled ? "bg-slate-900/90 backdrop-blur-lg shadow-lg" : "bg-transparent"
    )}>
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center">
          <Terminal className="h-6 w-6 text-emerald-500 mr-2" />
          <span className="font-mono font-bold text-xl">tref</span>
        </div>
        
        {/* Mobile menu button */}
        <button onClick={toggleMenu} className="lg:hidden text-emerald-500 hover:text-emerald-400 transition-colors">
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
        
        {/* Desktop navigation */}
        <nav className="hidden lg:block">
          <ul className="flex space-x-6 text-sm">
            <li><a href="#features" className="hover:text-emerald-500 transition-colors">Features</a></li>
            <li><a href="#examples" className="hover:text-emerald-500 transition-colors">Examples</a></li>
            <li><a href="#download" className="hover:text-emerald-500 transition-colors">Download</a></li>
            <li>
              <a 
                href="https://github.com/pavandhadge/tref" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-emerald-500 transition-colors"
              >
                GitHub
              </a>
            </li>
          </ul>
        </nav>
      </div>

      {/* Mobile navigation */}
      {isMenuOpen && (
        <div className="lg:hidden bg-slate-900 border-t border-slate-800">
          <nav className="px-4 py-4">
            <ul className="flex flex-col space-y-3">
              <li>
                <a 
                  href="#features" 
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-emerald-500 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Features
                </a>
              </li>
              <li>
                <a 
                  href="#examples" 
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-emerald-500 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Examples
                </a>
              </li>
              <li>
                <a 
                  href="#download" 
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-emerald-500 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Download
                </a>
              </li>
              <li>
                <a 
                  href="https://github.com/pavandhadge/tref" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-emerald-500 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  GitHub
                </a>
              </li>
            </ul>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
