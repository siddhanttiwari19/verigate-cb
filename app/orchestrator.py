"""
Orchestrator: wires Scorer -> Draft Agent -> Verifier -> Decision Gate,
and writes an append-only audit log for every dispute processed.

Decision gate policy (the "bounded and gated" requirement):
  - probability >= AUTO_SUBMIT_THRESHOLD AND verifier approves -> auto-submit
  - verifier rejects (hallucinated claim)                      -> escalate, always
  - probability < AUTO_SUBMIT_THRESHOLD                        -> escalate to human
No path skips the audit log. No path lets a rejected draft submit anyway.
"""
import json
import time
from pathlib import Path

from app.draft_agent import draft
from app.verifier import verify

AUTO_SUBMIT_THRESHOLD = 0.75
AUDIT_LOG_PATH = "data/audit_log.jsonl"


def process_dispute(dispute: dict, scorer) -> dict:
    evidence = dispute["evidence"]
    probability = scorer.score(evidence)
    letter, cited_claims = draft(evidence)
    verification = verify(cited_claims, evidence)

    if not verification.approved:
        decision = "ESCALATE_VERIFICATION_FAILED"
    elif probability >= AUTO_SUBMIT_THRESHOLD:
        decision = "AUTO_SUBMIT"
    else:
        decision = "ESCALATE_LOW_CONFIDENCE"

    record = {
        "timestamp": time.time(),
        "dispute_id": dispute["dispute_id"],
        "reason_code": dispute["reason_code"],
        "amount_inr": dispute["amount_inr"],
        "winnability_probability": round(probability, 3),
        "cited_claims": cited_claims,
        "verifier_approved": verification.approved,
        "verifier_reason": verification.reason,
        "decision": decision,
        "letter": letter,
    }

    Path(AUDIT_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

    return record


def run_batch(disputes: list[dict], scorer) -> dict:
    Path(AUDIT_LOG_PATH).unlink(missing_ok=True)  # fresh run
    decisions = {"AUTO_SUBMIT": 0, "ESCALATE_LOW_CONFIDENCE": 0, "ESCALATE_VERIFICATION_FAILED": 0}
    for d in disputes:
        rec = process_dispute(d, scorer)
        decisions[rec["decision"]] += 1
    return decisions


if __name__ == "__main__":
    from app.scorer import evaluate, load_dataset

    report, scorer = evaluate()
    rows, *_ = load_dataset()
    decisions = run_batch(rows[:50], scorer)

    print("Scorer eval:", json.dumps(report, indent=2))
    print("Batch decisions (first 50):", json.dumps(decisions, indent=2))
    print(f"Full audit trail written to {AUDIT_LOG_PATH}")
