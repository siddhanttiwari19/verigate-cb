export type Decision =
  | "AUTO_SUBMIT"
  | "ESCALATE_LOW_CONFIDENCE"
  | "ESCALATE_VERIFICATION_FAILED"
  | "ESCALATE_INTEGRITY_FAILED"
  | "ESCALATE_DRIFT_DETECTED";

export interface EvidenceFactor {
  factor: string;
  contribution: number;
  direction: "supports winning" | "hurts winning";
}

export interface Evidence {
  delivery_confirmation: boolean;
  signature_matches_cardholder: boolean;
  ip_matches_billing_country: boolean;
  prior_clean_order_count: number;
  support_chat_exists: boolean;
  refund_already_issued: boolean;
  device_fingerprint_reused: boolean;
}

export interface DisputeRecord {
  timestamp: number;
  dispute_id: string;
  reason_code: string;
  amount_inr: number;
  winnability_probability: number;
  threshold_applied: number;
  explanation: EvidenceFactor[];
  integrity_consistent: boolean;
  integrity_flags: string[];
  cited_claims: string[];
  verifier_approved: boolean;
  verifier_reason: string;
  drift_detected: boolean | null;
  decision: Decision;
  letter: string;
  evidence?: Evidence;
}
