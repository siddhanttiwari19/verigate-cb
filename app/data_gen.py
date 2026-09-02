"""
Generates a synthetic dataset of chargeback disputes + evidence artifacts.
Each dispute has a ground-truth 'winnable' label so the scorer can be
evaluated with real precision/recall on a held-out split.
"""
import json
import random
from pathlib import Path

random.seed(42)

REASON_CODES = ["product_not_received", "product_unacceptable", "fraud", "duplicate_charge"]

def make_dispute(dispute_id: int) -> dict:
    reason = random.choice(REASON_CODES)

    has_delivery_confirmation = random.random() < 0.6
    delivery_signature_matches_cardholder = has_delivery_confirmation and random.random() < 0.7
    ip_matches_billing_country = random.random() < 0.75
    prior_clean_order_count = random.choices([0, 1, 2, 5, 12], weights=[0.2, 0.2, 0.2, 0.2, 0.2])[0]
    support_chat_exists = random.random() < 0.4
    refund_already_issued = random.random() < 0.1
    device_fingerprint_reused = random.random() < 0.3

    # Ground truth heuristic (simulates what a real underwriting policy would say)
    score = 0
    score += 2 if has_delivery_confirmation else -1
    score += 2 if delivery_signature_matches_cardholder else 0
    score += 1 if ip_matches_billing_country else -1
    score += 1 if prior_clean_order_count >= 2 else 0
    score += 1 if device_fingerprint_reused else 0
    score -= 3 if refund_already_issued else 0
    score -= 2 if reason == "fraud" and not delivery_signature_matches_cardholder else 0

    winnable = score >= 3
    if random.random() < 0.12:  # simulate real-world label noise
        winnable = not winnable

    evidence = {
        "delivery_confirmation": has_delivery_confirmation,
        "signature_matches_cardholder": delivery_signature_matches_cardholder,
        "ip_matches_billing_country": ip_matches_billing_country,
        "prior_clean_order_count": prior_clean_order_count,
        "support_chat_exists": support_chat_exists,
        "refund_already_issued": refund_already_issued,
        "device_fingerprint_reused": device_fingerprint_reused,
    }

    return {
        "dispute_id": f"CB-{dispute_id:05d}",
        "reason_code": reason,
        "amount_inr": random.randint(299, 45000),
        "evidence": evidence,
        "label_winnable": winnable,  # ground truth, used only for eval
    }


def generate(n: int = 500, out_path: str = "data/disputes.jsonl"):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for i in range(n):
            f.write(json.dumps(make_dispute(i)) + "\n")
    print(f"wrote {n} synthetic disputes to {out_path}")


if __name__ == "__main__":
    generate()
