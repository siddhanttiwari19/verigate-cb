"""
Verifier Agent — the anti-hallucination gate.

The drafting agent writes a representment letter that cites specific
evidence claims (e.g. "signature on file matches cardholder"). Before
anything is allowed to reach the auto-submit path, the verifier checks
every cited claim against the *actual* retrieved evidence record.

If the draft claims something the evidence doesn't support, the whole
response is rejected and routed to human review — never silently
"corrected" by the LLM, because a self-corrected money-facing claim is
exactly the kind of thing that should have a human look at it.
"""
from dataclasses import dataclass, field

# Maps a claim tag the drafting agent is allowed to use -> the evidence
# field(s) that must be true for the claim to be verifiable.
CLAIM_REQUIREMENTS = {
    "DELIVERY_CONFIRMED": ["delivery_confirmation"],
    "SIGNATURE_MATCH": ["delivery_confirmation", "signature_matches_cardholder"],
    "IP_MATCH": ["ip_matches_billing_country"],
    "REPEAT_CUSTOMER": ["prior_clean_order_count"],  # checked numerically below
    "NO_PRIOR_REFUND": ["refund_already_issued"],    # must be False
}


@dataclass
class VerificationResult:
    approved: bool
    rejected_claims: list = field(default_factory=list)
    reason: str = ""


def verify(cited_claims: list[str], evidence: dict) -> VerificationResult:
    rejected = []

    for claim in cited_claims:
        if claim not in CLAIM_REQUIREMENTS:
            rejected.append(claim)  # unknown claim tag = auto-reject
            continue

        if claim == "REPEAT_CUSTOMER":
            if evidence.get("prior_clean_order_count", 0) < 2:
                rejected.append(claim)
            continue

        if claim == "NO_PRIOR_REFUND":
            if evidence.get("refund_already_issued", True):
                rejected.append(claim)
            continue

        required_fields = CLAIM_REQUIREMENTS[claim]
        if not all(evidence.get(f) for f in required_fields):
            rejected.append(claim)

    if rejected:
        return VerificationResult(
            approved=False,
            rejected_claims=rejected,
            reason=f"Draft cites {rejected} which the retrieved evidence does not support.",
        )
    return VerificationResult(approved=True, reason="All cited claims backed by evidence.")
