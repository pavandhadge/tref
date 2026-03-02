import { useState } from "react";
import { Terminal, Menu, X, Github } from "lucide-react";
import { Link as RouterLink, useLocation } from "react-router-dom";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { label: "Features", href: "/#features" },
    { label: "Examples", href: "/#examples" },
    { label: "Docs", href: "/docs" },
  ];

  const isDocs = location.pathname === "/docs";

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/70 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 w-full max-w-6xl items-center justify-between px-4">
        <RouterLink to="/" className="flex items-center gap-2">
          <div className="grid h-8 w-8 place-items-center rounded-lg bg-slate-900 text-white">
            <Terminal className="h-4 w-4" />
          </div>
          <span className="font-mono text-xl font-bold tracking-tight text-slate-900">tref</span>
        </RouterLink>

        <nav className="hidden items-center gap-7 lg:flex">
          {navItems.map((item) => (
            <a key={item.label} href={item.href} className="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900">
              {item.label}
            </a>
          ))}
          <a
            href="https://github.com/pavandhadge/tref"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 transition-colors hover:border-slate-900 hover:text-slate-900"
          >
            <Github className="h-4 w-4" />
            GitHub
          </a>
        </nav>

        <button
          className="grid h-9 w-9 place-items-center rounded-md border border-slate-300 text-slate-700 lg:hidden"
          onClick={() => setIsMenuOpen((v) => !v)}
          aria-label="Toggle menu"
        >
          {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {isMenuOpen && (
        <div className="border-t border-slate-200 bg-white lg:hidden">
          <nav className="mx-auto flex w-full max-w-6xl flex-col gap-1 px-4 py-3">
            {navItems.map((item) => (
              <a
                key={item.label}
                href={item.href}
                className="rounded-md px-2 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                onClick={() => setIsMenuOpen(false)}
              >
                {item.label}
              </a>
            ))}
            <a
              href="https://github.com/pavandhadge/tref"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md px-2 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              GitHub Repository
            </a>
          </nav>
        </div>
      )}

      {isDocs && <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-sky-300 to-transparent" />}
    </header>
  );
};

export default Header;
