import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function CtaSection() {
  return (
    <section className="px-6 md:px-16 py-28 text-center">
      <h2 className="font-display text-3xl md:text-4xl text-paper mb-6 max-w-xl mx-auto leading-tight">
        See a real dispute go through the gate.
      </h2>
      <p className="text-paper/65 max-w-md mx-auto mb-9 leading-relaxed">
        The console below runs on the same evidence, scoring, and verification logic —
        including one case the gate actually rejects.
      </p>
      <Link
        href="/console"
        className="inline-flex items-center gap-2 bg-accent text-paper rounded-lg px-6 py-3.5 text-sm font-medium hover:bg-accent-dim transition-colors"
      >
        Open the console
        <ArrowRight size={16} />
      </Link>
    </section>
  );
}
