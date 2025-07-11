
import { useState, useEffect } from "react";
import { Terminal, Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Link as RouterLink, useLocation } from "react-router-dom";

const scrollToSection = (id: string) => {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth" });
  }
};

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsMenuOpen(false); // close menu on route change
  }, [location]);

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

  const handleNav = (id: string) => {
    scrollToSection(id);
    setIsMenuOpen(false);
  };

  // Dynamic text color for contrast
  const navText = isScrolled ? "text-white" : "text-[#8B5CF6]";
  const navTextHover = isScrolled ? "hover:text-[#8B5CF6]" : "hover:text-[#0EA5E9]";

  return (
    <header className={cn(
      "sticky top-0 z-20 transition-all duration-300 backdrop-blur-xl",
      isScrolled ? "bg-slate-900/90 shadow-lg" : "bg-transparent"
    )}>
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <RouterLink to="/" className="flex items-center group">
          <Terminal className={cn("h-7 w-7 group-hover:scale-110 transition-transform mr-2", navText)} />
          <span className={cn("font-mono font-bold text-2xl tracking-tight", navText)}>tref</span>
        </RouterLink>
        {/* Mobile menu button */}
        <button onClick={() => setIsMenuOpen(!isMenuOpen)} className={cn("lg:hidden transition-colors", navText, navTextHover)}>
          {isMenuOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
        {/* Desktop navigation */}
        <nav className="hidden lg:block">
          <ul className="flex space-x-8 text-base font-mono">
            <li><button onClick={() => handleNav("features")} className={cn("transition-colors", navText, navTextHover)}>Features</button></li>
            <li><button onClick={() => handleNav("examples")} className={cn("transition-colors", navText, navTextHover)}>Examples</button></li>
            <li><RouterLink to="/docs" className={cn("transition-colors", navText, navTextHover)}>Docs</RouterLink></li>
            <li>
              <a 
                href="https://github.com/pavandhadge/tref" 
                target="_blank" 
                rel="noopener noreferrer"
                className={cn("transition-colors", navText, navTextHover)}
              >
                GitHub
              </a>
            </li>
            <li>
              <a
                href="https://github.com/pavandhadge/tref/releases"
                target="_blank"
                rel="noopener noreferrer"
                className={cn("transition-colors", navText, navTextHover)}
              >
                Download
              </a>
            </li>
          </ul>
        </nav>
      </div>
      {/* Mobile navigation */}
      {isMenuOpen && (
        <div className="lg:hidden bg-slate-900 border-t border-slate-800">
          <nav className="px-4 py-4">
            <ul className="flex flex-col space-y-3 font-mono">
              <li>
                <button 
                  onClick={() => handleNav("features")}
                  className="block px-2 py-2 w-full text-left hover:bg-slate-800 rounded hover:text-[#8B5CF6] transition-colors"
                >
                  Features
                </button>
              </li>
              <li>
                <button 
                  onClick={() => handleNav("examples")}
                  className="block px-2 py-2 w-full text-left hover:bg-slate-800 rounded hover:text-[#8B5CF6] transition-colors"
                >
                  Examples
                </button>
              </li>
              <li>
                <RouterLink 
                  to="/docs"
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-[#8B5CF6] transition-colors"
                >
                  Docs
                </RouterLink>
              </li>
              <li>
                <a 
                  href="https://github.com/pavandhadge/tref" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-[#8B5CF6] transition-colors"
                >
                  GitHub
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/pavandhadge/tref/releases"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block px-2 py-2 hover:bg-slate-800 rounded hover:text-[#8B5CF6] transition-colors"
                >
                  Download
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
