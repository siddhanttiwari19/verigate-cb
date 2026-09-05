import { Evidence } from "@/types/dispute";
import { Check, X } from "lucide-react";

const LABELS: Record<keyof Evidence, string> = {
  delivery_confirmation: "Delivery confirmation on file",
  signature_matches_cardholder: "Signature matches cardholder",
  ip_matches_billing_country: "IP matches billing country",
  prior_clean_order_count: "Prior clean orders",
  support_chat_exists: "Support chat log exists",
  refund_already_issued: "Refund already issued",
  device_fingerprint_reused: "Device fingerprint reused",
};

export function EvidenceChecklist({ evidence }: { evidence: Evidence }) {
  const entries = Object.entries(evidence) as [keyof Evidence, boolean | number][];

  return (
    <ul className="divide-y divide-paper/10">
      {entries.map(([key, value]) => {
        const isCount = typeof value === "number";
        const isTrue = isCount ? value > 0 : value === true;

        return (
          <li key={key} className="flex items-center justify-between py-2.5">
            <span className="text-sm text-paper/85">{LABELS[key]}</span>
            {isCount ? (
              <span className="font-data text-sm text-paper/90 tabular-nums">{value}</span>
            ) : isTrue ? (
              <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-verified-dim text-verified">
                <Check size={13} strokeWidth={3} />
              </span>
            ) : (
              <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-ink-raised text-slate">
                <X size={13} strokeWidth={3} />
              </span>
            )}
          </li>
        );
      })}
    </ul>
  );
}
