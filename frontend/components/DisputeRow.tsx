"use client";

import { motion } from "framer-motion";
import { DisputeRecord } from "@/types/dispute";
import { DecisionBadge } from "./DecisionBadge";

interface DisputeRowProps {
  dispute: DisputeRecord;
  isActive: boolean;
  onSelect: () => void;
  index: number;
}

export function DisputeRow({ dispute, isActive, onSelect, index }: DisputeRowProps) {
  return (
    <motion.button
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.04, duration: 0.25, ease: "easeOut" }}
      onClick={onSelect}
      className={`w-full text-left px-4 py-3.5 border-b border-paper/10 transition-colors
        ${isActive ? "bg-ink-raised" : "hover:bg-ink-raised/50"}`}
    >
      <div className="flex items-center justify-between mb-1.5">
        <span className="font-data text-sm text-paper/90">{dispute.dispute_id}</span>
        <span className="font-data text-xs text-slate tabular-nums">
          ₹{dispute.amount_inr.toLocaleString("en-IN")}
        </span>
      </div>
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs text-slate capitalize truncate">
          {dispute.reason_code.replaceAll("_", " ")}
        </span>
      </div>
      <div className="mt-2">
        <DecisionBadge decision={dispute.decision} />
      </div>
    </motion.button>
  );
}