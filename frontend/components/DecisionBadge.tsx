import { Decision } from "@/types/dispute";
import { CheckCircle2, AlertTriangle, ShieldAlert, TrendingDown, Activity } from "lucide-react";

const DECISION_META: Record<
  Decision,
  { label: string; tone: "verified" | "rejected"; icon: typeof CheckCircle2 }
> = {
  AUTO_SUBMIT: { label: "Auto-submitted", tone: "verified", icon: CheckCircle2 },
  ESCALATE_LOW_CONFIDENCE: { label: "Escalated · low confidence", tone: "rejected", icon: TrendingDown },
  ESCALATE_VERIFICATION_FAILED: { label: "Escalated · verifier rejected", tone: "rejected", icon: ShieldAlert },
  ESCALATE_INTEGRITY_FAILED: { label: "Escalated · integrity flag", tone: "rejected", icon: AlertTriangle },
  ESCALATE_DRIFT_DETECTED: { label: "Escalated · drift detected", tone: "rejected", icon: Activity },
};

export function DecisionBadge({ decision }: { decision: Decision }) {
  const meta = DECISION_META[decision];
  const Icon = meta.icon;
  const isVerified = meta.tone === "verified";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
        isVerified
          ? "bg-verified-dim text-verified"
          : "bg-rejected-dim text-rejected"
      }`}
    >
      <Icon size={13} strokeWidth={2.25} />
      {meta.label}
    </span>
  );
}
