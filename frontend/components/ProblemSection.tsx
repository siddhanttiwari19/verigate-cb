"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { FileWarning, Scale, Users } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const POINTS = [
  {
    icon: FileWarning,
    title: "Most chargebacks are winnable",
    body: "The evidence exists — delivery confirmation, order history, IP match. Nobody has twenty minutes per case to write it up.",
  },
  {
    icon: Scale,
    title: "Money-facing AI needs a harder bar",
    body: "A hallucinated claim in a support ticket is annoying. A hallucinated claim in a legal-financial dispute response is a liability.",
  },
  {
    icon: Users,
    title: "The fix isn't more automation",
    body: "It's a system that knows when to distrust its own draft, and hands off to a person instead of guessing.",
  },
];

export function ProblemSection() {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".problem-item", {
        opacity: 0,
        y: 24,
        duration: 0.6,
        stagger: 0.12,
        ease: "power2.out",
        scrollTrigger: {
          trigger: ref.current,
          start: "top 70%",
        },
      });
    }, ref);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={ref} className="px-6 md:px-16 py-28">
      <div className="max-w-5xl mx-auto">
        <h2 className="font-display text-3xl md:text-4xl text-paper mb-16 max-w-lg">
          Why this needed a gate, not just a smarter draft.
        </h2>
        <div className="grid md:grid-cols-3 gap-10">
          {POINTS.map((point) => (
            <div key={point.title} className="problem-item">
              <point.icon size={22} className="text-accent mb-4" strokeWidth={1.75} />
              <h3 className="text-paper font-medium mb-2.5">{point.title}</h3>
              <p className="text-sm text-paper/65 leading-relaxed">{point.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
