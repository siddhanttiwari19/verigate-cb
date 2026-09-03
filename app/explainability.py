"""
Feature 3 — Per-Decision Explainability.

The scorer is a logistic regression, which means its coefficients ARE
the explanation — no need for a separate SHAP/LIME dependency. This
turns (coefficient x feature value) into a ranked, human-readable list
of what pushed the decision toward "winnable" or "not winnable", so a
human reviewer looking at an escalated case doesn't have to guess why
the model said what it said.
"""
from app.scorer import FEATURES

READABLE_NAMES = {
    "delivery_confirmation": "Delivery confirmation on file",
    "signature_matches_cardholder": "Signature matches cardholder",
    "ip_matches_billing_country": "IP matches billing country",
    "prior_clean_order_count": "Prior clean order history",
    "support_chat_exists": "Support chat log exists",
    "refund_already_issued": "Refund already issued",
    "device_fingerprint_reused": "Device fingerprint reused",
}


def explain(evidence: dict, model) -> list[dict]:
    """
    Returns each feature's contribution to the winnability log-odds,
    sorted by magnitude (largest impact first). Positive = pushed
    toward "winnable", negative = pushed toward "not winnable".
    """
    coefs = model.coef_[0]
    contributions = []

    for feature, coef in zip(FEATURES, coefs):
        value = float(evidence.get(feature, 0))
        contribution = round(coef * value, 3)
        if contribution == 0:
            continue
        contributions.append({
            "factor": READABLE_NAMES.get(feature, feature),
            "contribution": contribution,
            "direction": "supports winning" if contribution > 0 else "hurts winning",
        })

    contributions.sort(key=lambda c: abs(c["contribution"]), reverse=True)
    return contributions
