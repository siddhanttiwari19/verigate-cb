"""
Orchestrator v2 — wires every stage together:

  integrity check -> scorer -> explainability -> dynamic threshold
  -> draft -> verifier -> drift monitor -> decision gate -> audit log

Decision gate policy:
  - evidence fails integrity check              -> escalate, always
  - verifier rejects (hallucinated claim)        -> escalate, always
  - drift detected                               -> escalate regardless of confidence
  - probability >= dynamic threshold for amount  -> auto-submit
  - otherwise                                    -> escalate to human

No path skips the audit log. No path lets a rejected/inconsistent draft
submit anyway.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from app.config import settings
from app.draft_agent import draft
from app.drift_monitor import DriftMonitor
from app.dynamic_threshold import dynamic_threshold
from app.evidence_integrity import check_integrity
from app.explainability import explain
from app.verifier import verify


def process_dispute(dispute: dict, scorer, drift_monitor: DriftMonitor | None = None) -> dict:
    evidence = dispute["evidence"]
    amount = dispute["amount_inr"]

    integrity = check_integrity(evidence)
    probability = scorer.score(evidence)
    explanation = explain(evidence, scorer.model)
    threshold = dynamic_threshold(amount)
    letter, cited_claims = draft(evidence)
    verification = verify(cited_claims, evidence)

    drift_status = drift_monitor.record(probability) if drift_monitor else None

    if not integrity.is_consistent:
        decision = "ESCALATE_INTEGRITY_FAILED"
    elif not verification.approved:
        decision = "ESCALATE_VERIFICATION_FAILED"
    elif drift_status and drift_status.drifted:
        decision = "ESCALATE_DRIFT_DETECTED"
    elif probability >= threshold:
        decision = "AUTO_SUBMIT"
    else:
        decision = "ESCALATE_LOW_CONFIDENCE"

    record = {
        "timestamp": time.time(),
        "dispute_id": dispute["dispute_id"],
        "reason_code": dispute["reason_code"],
        "amount_inr": amount,
        "winnability_probability": round(probability, 3),
        "threshold_applied": round(threshold, 3),
        "explanation": explanation,
        "integrity_consistent": integrity.is_consistent,
        "integrity_flags": integrity.flags,
        "cited_claims": cited_claims,
        "verifier_approved": verification.approved,
        "verifier_reason": verification.reason,
        "drift_detected": drift_status.drifted if drift_status else None,
        "decision": decision,
        "letter": letter,
    }

    Path(settings.audit_log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(settings.audit_log_path, "a") as f:
        f.write(json.dumps(record) + "\n")

    return record


def run_batch(disputes: list[dict], scorer, baseline_mean: float, baseline_std: float) -> dict:
    Path(settings.audit_log_path).unlink(missing_ok=True)  # fresh run
    monitor = DriftMonitor(baseline_mean=baseline_mean, baseline_std=baseline_std)

    decisions = {
        "AUTO_SUBMIT": 0,
        "ESCALATE_LOW_CONFIDENCE": 0,
        "ESCALATE_VERIFICATION_FAILED": 0,
        "ESCALATE_INTEGRITY_FAILED": 0,
        "ESCALATE_DRIFT_DETECTED": 0,
    }
    for d in disputes:
        rec = process_dispute(d, scorer, monitor)
        decisions[rec["decision"]] += 1
    return decisions


if __name__ == "__main__":
    import numpy as np

    from app.scorer import evaluate, load_dataset

    report, scorer = evaluate()
    rows, X, y, amounts = load_dataset()
    probs = scorer.model.predict_proba(X)[:, 1]
    baseline_mean, baseline_std = float(np.mean(probs)), float(np.std(probs))

    decisions = run_batch(rows, scorer, baseline_mean, baseline_std)

    print("Scorer eval:", json.dumps(report, indent=2))
    print("Batch decisions (all disputes):", json.dumps(decisions, indent=2))
    print(f"Full audit trail written to {settings.audit_log_path}")
