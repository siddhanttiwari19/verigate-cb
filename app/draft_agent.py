"""
Drafting Agent.

Ships with a deterministic template so the pipeline runs end-to-end
with zero API keys (needed for grading / demo reliability). Swap
`draft()` for a real LLM call (Claude, GPT, etc.) when you want richer
prose — the verifier gate downstream doesn't care which one produced
the draft, it checks the same way either way.
"""

def draft(evidence: dict) -> tuple[str, list[str]]:
    """Returns (letter_text, cited_claim_tags)."""
    claims = []
    lines = []

    if evidence.get("delivery_confirmation"):
        claims.append("DELIVERY_CONFIRMED")
        lines.append("- Delivery confirmation is on file for this order.")
    if evidence.get("delivery_confirmation") and evidence.get("signature_matches_cardholder"):
        claims.append("SIGNATURE_MATCH")
        lines.append("- The delivery signature matches the cardholder's name on file.")
    if evidence.get("ip_matches_billing_country"):
        claims.append("IP_MATCH")
        lines.append("- The originating IP address for this order matches the billing country.")
    if evidence.get("prior_clean_order_count", 0) >= 2:
        claims.append("REPEAT_CUSTOMER")
        count = evidence['prior_clean_order_count']
        lines.append(f"- The cardholder has {count} prior clean orders with no disputes.")
    if not evidence.get("refund_already_issued"):
        claims.append("NO_PRIOR_REFUND")
        lines.append("- No refund has been issued for this transaction.")

    if not lines:
        letter = "Insufficient evidence to contest this dispute. Recommend accepting the chargeback."
    else:
        intro = "We respectfully submit the following evidence in response to this dispute:"
        letter = intro + "\n" + "\n".join(lines)

    return letter, claims
