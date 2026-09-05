"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const STATS = [
  { value: 93.4, suffix: "%", label: "Precision on held-out disputes" },
  { value: 86.6, suffix: "%", label: "Recall on held-out disputes" },
  { value: 21, suffix: "", label: "Inconsistent evidence records caught before scoring" },
];

export function StatsSection() {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const counters = gsap.utils.toArray<HTMLElement>(".stat-value");
      counters.forEach((el) => {
        const target = parseFloat(el.dataset.value ?? "0");
        const obj = { val: 0 };
        gsap.to(obj, {
          val: target,
          duration: 1.4,
          ease: "power2.out",
          scrollTrigger: { trigger: el, start: "top 85%" },
          onUpdate: () => {
            el.textContent = obj.val.toFixed(target % 1 !== 0 ? 1 : 0);
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={ref} className="px-6 md:px-16 py-24 border-y border-paper/10">
      <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-12">
        {STATS.map((stat) => (
          <div key={stat.label}>
            <p className="font-data text-5xl text-paper tabular-nums">
              <span className="stat-value" data-value={stat.value}>
                0
              </span>
              {stat.suffix}
            </p>
            <p className="text-sm text-slate mt-3 leading-relaxed max-w-[220px]">{stat.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
