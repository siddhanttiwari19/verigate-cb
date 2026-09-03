"""
Feature 1 — Evidence Integrity Checker.

Runs BEFORE the scorer even sees the evidence. Catches records that are
internally inconsistent — the kind of thing that indicates a data entry
error, a tampered record, or a bug upstream, rather than a genuine
weak-evidence case. This is different from the verifier (which checks
the *draft* against evidence) — this checks the *evidence itself* for
self-contradiction.
"""
from dataclasses import dataclass, field


@dataclass
class IntegrityResult:
    is_consistent: bool
    flags: list[str] = field(default_factory=list)


def check_integrity(evidence: dict) -> IntegrityResult:
    flags = []

    # A signature match is logically impossible without a delivery confirmation.
    if evidence.get("signature_matches_cardholder") and not evidence.get("delivery_confirmation"):
        flags.append("signature_match_without_delivery_confirmation")

    # A refund already issued but the merchant is still contesting via evidence
    # with zero disqualifying signal elsewhere is a workflow contradiction —
    # someone is either fighting a dispute they already refunded, or the
    # refund flag is stale/wrong.
    if evidence.get("refund_already_issued") and evidence.get("prior_clean_order_count", 0) == 0 \
            and not evidence.get("support_chat_exists"):
        flags.append("refund_issued_with_no_supporting_context")

    # Negative or absurd order counts indicate a data pipeline bug, not a
    # real customer.
    prior_orders = evidence.get("prior_clean_order_count", 0)
    if prior_orders < 0 or prior_orders > 1000:
        flags.append("implausible_prior_order_count")

    # Device fingerprint reuse combined with a cardholder-matching signature
    # is a real contradiction worth a human's eyes — reused device usually
    # signals account sharing or fraud rings, not the legitimate cardholder.
    if evidence.get("device_fingerprint_reused") and evidence.get("signature_matches_cardholder") \
            and evidence.get("prior_clean_order_count", 0) == 0:
        flags.append("device_reuse_with_first_time_signature_match")

    return IntegrityResult(is_consistent=len(flags) == 0, flags=flags)
