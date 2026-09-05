"use client";

import { motion } from "framer-motion";

interface StampProps {
  approved: boolean;
  disputeId: string;
}

/**
 * This is the one place the design spends its boldness. Everything else in
 * the console is quiet and legible on purpose — but the verifier's verdict
 * is the entire reason this product exists, so it gets a physical, literal
 * treatment: a stamp on the document, the way a real auditor would mark one.
 */
export function Stamp({ approved, disputeId }: StampProps) {
  return (
    <motion.div
      key={disputeId} // re-triggers the snap-in whenever the selected dispute changes
      initial={{ opacity: 0, scale: 1.4, rotate: approved ? -8 : 6 }}
      animate={{ opacity: 1, scale: 1, rotate: approved ? -8 : 6 }}
      transition={{ type: "spring", stiffness: 380, damping: 18, delay: 0.15 }}
      className={`pointer-events-none select-none inline-flex items-center justify-center
        border-[3px] rounded-md px-4 py-1.5 font-display font-semibold italic text-lg tracking-wide
        ${approved ? "border-verified text-verified" : "border-rejected text-rejected"}`}
      style={{ mixBlendMode: "normal" }}
      aria-label={approved ? "Verifier approved" : "Verifier rejected"}
    >
      {approved ? "VERIFIED" : "REJECTED"}
    </motion.div>
  );
}
