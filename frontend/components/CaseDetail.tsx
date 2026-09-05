"use client";

import { AnimatePresence, motion } from "framer-motion";
import { DisputeRecord } from "@/types/dispute";
import { DecisionBadge } from "./DecisionBadge";
import { Stamp } from "./Stamp";
import { ExplainabilityBars } from "./ExplainabilityBars";
import { EvidenceChecklist } from "./EvidenceChecklist";
import { AlertTriangle } from "lucide-react";

export function CaseDetail({ dispute }: { dispute: DisputeRecord | null }) {
  if (!dispute) {
    return (
      <div className="flex-1 flex items-center justify-center text-slate text-sm">
        Select a dispute from the queue to review its case file.
      </div>
    );
  }

  const probabilityPct = Math.round(dispute.winnability_probability * 100);
  const thresholdPct = Math.round(dispute.threshold_applied * 100);

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={dispute.dispute_id}
        initial={{ opacity: 0, x: 12 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -12 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
        className="flex-1 overflow-y-auto"
      >
        {/* Header */}
        <div className="px-8 pt-8 pb-6 border-b border-paper/10">
          <div className="flex items-start justify-between gap-4 mb-3">
            <div>
              <h1 className="font-data text-2xl text-paper mb-1">{dispute.dispute_id}</h1>
              <p className="text-sm text-slate capitalize">
                {dispute.reason_code.replaceAll("_", " ")} · ₹{dispute.amount_inr.toLocaleString("en-IN")}
              </p>
            </div>
            <DecisionBadge decision={dispute.decision} />
          </div>

          {!dispute.integrity_consistent && (
            <div className="mt-4 flex items-start gap-2.5 rounded-lg bg-rejected-dim/60 border border-rejected/30 px-3.5 py-3">
              <AlertTriangle size={16} className="text-rejected shrink-0 mt-0.5" />
              <div>
                <p className="text-sm text-rejected font-medium">Evidence integrity flagged</p>
                <p className="text-xs text-paper/70 mt-0.5">
                  {dispute.integrity_flags.join(", ").replaceAll("_", " ")}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Confidence + threshold */}
        <div className="px-8 py-6 border-b border-paper/10">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-xs text-slate uppercase tracking-wide mb-1.5">Winnability</p>
              <p className="font-data text-3xl text-paper tabular-nums">{probabilityPct}%</p>
            </div>
            <div>
              <p className="text-xs text-slate uppercase tracking-wide mb-1.5">Required for this amount</p>
              <p className="font-data text-3xl text-slate tabular-nums">{thresholdPct}%</p>
            </div>
          </div>
        </div>

        {/* Explainability */}
        <div className="px-8 py-6 border-b border-paper/10">
          <p className="text-xs text-slate uppercase tracking-wide mb-4">What drove this score</p>
          <ExplainabilityBars factors={dispute.explanation} />
        </div>

        {/* Evidence checklist */}
        {dispute.evidence && (
          <div className="px-8 py-6 border-b border-paper/10">
            <p className="text-xs text-slate uppercase tracking-wide mb-2">Evidence on file</p>
            <EvidenceChecklist evidence={dispute.evidence} />
          </div>
        )}

        {/* The letter + the stamp */}
        <div className="px-8 py-6">
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs text-slate uppercase tracking-wide">Drafted response</p>
            <Stamp approved={dispute.verifier_approved} disputeId={dispute.dispute_id} />
          </div>
          <div className="rounded-lg bg-ink-raised border border-paper/10 px-5 py-4">
            <p className="text-sm text-paper/85 leading-relaxed whitespace-pre-line">
              {dispute.letter}
            </p>
          </div>
          <p className="text-xs text-slate mt-3 leading-relaxed">{dispute.verifier_reason}</p>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
