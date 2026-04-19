import { Github } from "lucide-react";

const Footer = () => {
  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="mx-auto grid w-full max-w-6xl gap-8 px-4 py-10 md:grid-cols-2 md:items-end">
        <div>
          <div className="font-mono text-2xl font-bold text-slate-900">tref</div>
          <p className="mt-2 max-w-md text-sm text-slate-600">
            Offline-first versioned developer reference. Query docs snapshots with trust-aware updates and structured output.
          </p>
        </div>

        <div className="md:text-right">
          <p className="text-sm text-slate-600">Built by Pavan Dhadge</p>
          <a
            href="https://github.com/pavandhadge/tref"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-2 inline-flex items-center gap-2 text-sm font-medium text-slate-900 hover:text-sky-700"
          >
            <Github className="h-4 w-4" />
            github.com/pavandhadge/tref
          </a>
          <p className="mt-4 text-xs text-slate-500">ApacheLicense</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
