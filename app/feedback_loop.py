"""
Feature 5 — Human Feedback Loop.

The scorer is frozen at training time and never learns from what
actually happens to a dispute after the model made its call. This
lets a human reviewer record the real outcome (won / lost) for any
dispute, building a labeled dataset over time that a retraining job
can consume — closing the loop instead of the model staying static
forever.
"""
import json
import time
from pathlib import Path

from app.config import settings


def record_outcome(dispute_id: str, actual_outcome: str, reviewer_note: str = "") -> dict:
    """
    actual_outcome must be 'won' or 'lost'. This is intentionally
    separate from the audit log (which records the SYSTEM's decision
    at the time) — this file records what REALLY happened, which is
    often known days or weeks later.
    """
    if actual_outcome not in ("won", "lost"):
        raise ValueError("actual_outcome must be 'won' or 'lost'")

    record = {
        "timestamp": time.time(),
        "dispute_id": dispute_id,
        "actual_outcome": actual_outcome,
        "reviewer_note": reviewer_note,
    }

    Path(settings.feedback_log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(settings.feedback_log_path, "a") as f:
        f.write(json.dumps(record) + "\n")

    return record


def retraining_readiness() -> dict:
    """
    Reports how much labeled feedback has accumulated, so you know
    when there's enough real-world signal to justify retraining the
    scorer instead of relying purely on synthetic data.
    """
    path = Path(settings.feedback_log_path)
    if not path.exists():
        return {"feedback_records": 0, "ready_to_retrain": False}

    count = sum(1 for _ in open(path))
    # Rule of thumb threshold — tune once you know your real dispute volume.
    MIN_RECORDS_FOR_RETRAIN = 100
    return {
        "feedback_records": count,
        "ready_to_retrain": count >= MIN_RECORDS_FOR_RETRAIN,
        "records_needed": max(0, MIN_RECORDS_FOR_RETRAIN - count),
    }
