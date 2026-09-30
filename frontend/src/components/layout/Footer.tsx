import { useState } from "react";
import { ExternalLink, FileText } from "lucide-react";
import { TermsModal } from "../TermsModal";

export function Footer({ className = "" }: { className?: string }) {
  const [showTerms, setShowTerms] = useState(false);

  return (
    <>
      <footer
        className={`flex flex-wrap items-center justify-between gap-3 border-t border-[#e8e4dc] bg-white px-4 py-3 text-xs text-neutral-500 ${className}`}
      >
        <div className="flex items-center gap-1.5 font-medium">
          <span>Melitrack © {new Date().getFullYear()}</span>
          <span>•</span>
          <span className="inline-flex items-center gap-1">
            Desenvolvido por{" "}
            <a
              href="https://www.linkedin.com/in/lucas-blanger-4668a2210/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-0.5 font-semibold text-[#1D6A4A] transition-colors hover:underline hover:text-[#155438]"
            >
              Lucas Blanger
              <ExternalLink size={10} />
            </a>
          </span>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => setShowTerms(true)}
            className="inline-flex items-center gap-1 text-neutral-500 transition-colors hover:text-[#1D6A4A] hover:underline"
          >
            <FileText size={12} />
            Termos de Serviço
          </button>
        </div>
      </footer>

      <TermsModal isOpen={showTerms} onClose={() => setShowTerms(false)} />
    </>
  );
}
