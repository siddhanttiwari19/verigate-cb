"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Check } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const CLAIMS = [
  { id: "delivery", label: "Delivery confirmation is on file for this order." },
  { id: "signature", label: "The delivery signature matches the cardholder's name." },
  { id: "ip", label: "The originating IP address matches the billing country." },
];

const CAPTIONS = [
  "The drafting agent writes a response, citing specific evidence claims — same as any AI drafting tool.",
  "But before anything ships, a second agent checks every claim against the actual retrieved evidence record.",
  "If a claim doesn't hold up, the whole response is rejected — not silently rewritten — and a person reviews it instead.",
  "Only what's fully verified gets stamped and sent. That's the entire point of the gate.",
];

export function GateSection() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
  const ctx = gsap.context(() => {
    const claimEls = gsap.utils.toArray<HTMLElement>(
      ".gate-claim-check"
    );

    const captionEls = gsap.utils.toArray<HTMLElement>(
      ".gate-caption"
    );

    // Initial state
    gsap.set(claimEls, {
      autoAlpha: 0,
      scale: 0.4,
    });

    // IMPORTANT: Hide ALL captions initially
    gsap.set(captionEls, {
      autoAlpha: 0,
      y: 8,
    });

    gsap.set(".gate-stamp", {
      autoAlpha: 0,
      scale: 1.6,
      rotate: -18,
    });

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionRef.current,
        start: "top top",
        end: "+=2200",
        scrub: 0.6,
        pin: true,
        anticipatePin: 1,
      },
    });

    // Show first caption
    tl.to(captionEls[0], {
      autoAlpha: 1,
      y: 0,
      duration: 0.3,
    });

    // First claim
    tl.to(
      claimEls[0],
      {
        autoAlpha: 1,
        scale: 1,
        duration: 0.35,
        ease: "back.out(2)",
      },
      "+=0.2"
    );

    // Remaining claims
    for (let i = 1; i < claimEls.length; i++) {
      // Completely hide previous caption
      tl.to(
        captionEls[i - 1],
        {
          autoAlpha: 0,
          y: -8,
          duration: 0.25,
        },
        "+=0.15"
      );

      // Show next caption
      tl.to(
        captionEls[i],
        {
          autoAlpha: 1,
          y: 0,
          duration: 0.3,
        },
        "<"
      );

      // Show checkmark
      tl.to(
        claimEls[i],
        {
          autoAlpha: 1,
          scale: 1,
          duration: 0.35,
          ease: "back.out(2)",
        },
        "+=0.1"
      );
    }

    // Hide third caption
    tl.to(
      captionEls[2],
      {
        autoAlpha: 0,
        y: -8,
        duration: 0.25,
      },
      "+=0.2"
    );

    // Show final caption
    tl.to(
      captionEls[3],
      {
        autoAlpha: 1,
        y: 0,
        duration: 0.3,
      },
      "<"
    );

    // Show VERIFIED stamp
    tl.to(
      ".gate-stamp",
      {
        autoAlpha: 1,
        scale: 1,
        rotate: -8,
        duration: 0.5,
        ease: "back.out(1.8)",
      },
      "+=0.2"
    );

    // Change border color
    tl.to(
      ".gate-letter-card",
      {
        borderColor: "var(--color-verified)",
        duration: 0.3,
      },
      "<"
    );
  }, sectionRef);

  return () => ctx.revert();
}, []);

  return (
    <section id="gate" ref={sectionRef} className="relative min-h-screen flex items-center px-6 md:px-16 py-20">
      <div className="grid md:grid-cols-2 gap-16 items-center max-w-6xl mx-auto w-full">
        {/* Caption column */}
        <div className="relative h-40">
          {CAPTIONS.map((caption, i) => (
            <p
              key={i}
              className="gate-caption absolute inset-0 opacity-0 text-xl md:text-2xl text-paper/90 leading-snug font-display"
            >
              {caption}
            </p>
          ))}
        </div>

        {/* Visual: the draft letter with claims + stamp */}
        <div className="relative">
          <div className="gate-letter-card rounded-xl border-2 border-paper/15 bg-ink-raised px-7 py-8 transition-colors">
            <p className="text-xs text-slate uppercase tracking-wide mb-5">Drafted response</p>
            <ul className="space-y-4">
              {CLAIMS.map((claim) => (
                <li key={claim.id} className="flex items-start gap-3">
                  <span className="gate-claim-check mt-0.5 inline-flex items-center justify-center w-5 h-5 rounded-full bg-verified-dim text-verified shrink-0">
                    <Check size={13} strokeWidth={3} />
                  </span>
                  <span className="text-sm text-paper/80 leading-relaxed">{claim.label}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="gate-stamp absolute -right-4 -bottom-6 md:-right-8 md:-bottom-8">
            <div className="border-[3px] border-verified text-verified rounded-md px-5 py-2 font-display italic text-xl -rotate-8 bg-ink/80">
              VERIFIED
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
