"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function Hero() {
  const containerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

      tl.from(".hero-eyebrow", { opacity: 0, y: 10, duration: 0.5 })
        .from(
          ".hero-line",
          { opacity: 0, y: 28, duration: 0.7, stagger: 0.08 },
          "-=0.2"
        )
        .from(".hero-sub", { opacity: 0, y: 14, duration: 0.5 }, "-=0.3")
        .from(".hero-cta", { opacity: 0, y: 10, duration: 0.5 }, "-=0.25")
        .from(
          ".hero-stamp-preview",
          { opacity: 0, scale: 1.3, rotate: -14, duration: 0.6, ease: "back.out(1.7)" },
          "-=0.4"
        );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={containerRef} className="relative min-h-screen flex items-center px-6 md:px-16 overflow-hidden">
      {/* Faint background grid — texture only, no motion */}
      <div
        className="absolute inset-0 opacity-[0.04] pointer-events-none"
        style={{
          backgroundImage:
            "linear-gradient(#f7f5f0 1px, transparent 1px), linear-gradient(90deg, #f7f5f0 1px, transparent 1px)",
          backgroundSize: "56px 56px",
        }}
      />

      <div className="relative max-w-3xl">
        <p className="hero-eyebrow text-sm text-accent font-medium mb-6">
          For chargeback response teams
        </p>
        <h1 className="font-display text-5xl md:text-6xl leading-[1.08] text-paper mb-6">
          <span className="hero-line block">Chargeback evidence,</span>
          <span className="hero-line block italic text-slate">verified before it&apos;s sent.</span>
        </h1>
        <p className="hero-sub text-lg text-paper/70 max-w-xl leading-relaxed mb-9">
          Most AI response tools trust their own draft. Verigate doesn&apos;t — every claim it
          writes gets checked against the actual evidence record before anything reaches a
          customer, and anything it can&apos;t prove gets handed to a person instead.
        </p>
        <div className="hero-cta flex items-center gap-4">
          <Link
            href="/console"
            className="inline-flex items-center gap-2 bg-accent text-paper rounded-lg px-5 py-3 text-sm font-medium hover:bg-accent-dim transition-colors"
          >
            Open the console
            <ArrowRight size={16} />
          </Link>
          <a
            href="#gate"
            className="text-sm text-paper/70 hover:text-paper transition-colors"
          >
            See how the gate works
          </a>
        </div>
      </div>

      <div className="hero-stamp-preview hidden lg:block absolute right-16 top-1/2 -translate-y-1/2">
        <div className="border-[3px] border-verified text-verified rounded-md px-6 py-2.5 font-display italic text-2xl -rotate-6">
          VERIFIED
        </div>
      </div>
    </div>
  );
}
