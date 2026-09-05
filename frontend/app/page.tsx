import { Hero } from "@/components/Hero";
import { ProblemSection } from "@/components/ProblemSection";
import { GateSection } from "@/components/GateSection";
import { StatsSection } from "@/components/StatsSection";
import { CtaSection } from "@/components/CtaSection";

export default function LandingPage() {
  return (
    <main className="bg-ink">
      <Hero />
      <ProblemSection />
      <GateSection />
      <StatsSection />
      <CtaSection />
    </main>
  );
}