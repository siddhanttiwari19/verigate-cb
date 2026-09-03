"""
Evidence Scorer: turns a dispute's evidence dict into a calibrated
probability that the merchant wins the chargeback if they respond.

Trained on the synthetic dataset so precision/recall are measurable,
not asserted.
"""
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "delivery_confirmation",
    "signature_matches_cardholder",
    "ip_matches_billing_country",
    "prior_clean_order_count",
    "support_chat_exists",
    "refund_already_issued",
    "device_fingerprint_reused",
]


def load_dataset(path: str = "data/disputes.jsonl"):
    rows = [json.loads(line) for line in open(path)]
    X = np.array([[float(r["evidence"][f]) for f in FEATURES] for r in rows])
    y = np.array([int(r["label_winnable"]) for r in rows])
    amounts = np.array([r["amount_inr"] for r in rows])
    return rows, X, y, amounts


class EvidenceScorer:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def score(self, evidence: dict) -> float:
        x = np.array([[float(evidence[f]) for f in FEATURES]])
        return float(self.model.predict_proba(x)[0][1])


def evaluate(threshold: float = 0.6, path: str = "data/disputes.jsonl"):
    rows, X, y, amounts = load_dataset(path)
    X_train, X_test, y_train, y_test, amt_train, amt_test = train_test_split(
        X, y, amounts, test_size=0.3, random_state=7, stratify=y
    )

    scorer = EvidenceScorer().fit(X_train, y_train)
    probs = scorer.model.predict_proba(X_test)[:, 1]
    preds = (probs >= threshold).astype(int)

    precision = precision_score(y_test, preds, zero_division=0)
    recall = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()

    # False positives = we auto-submitted a response that then lost.
    # That has a real cost: representment fee + wasted ops time.
    REPRESENTMENT_FEE_INR = 500
    false_positive_cost = int(fp) * REPRESENTMENT_FEE_INR

    # Money left on the table = disputes we *could* have won but
    # the gate sent to manual review or didn't flag (false negatives).
    recovered_if_perfect = int(amt_test[(y_test == 1)].sum())
    recovered_by_model = int(amt_test[(preds == 1) & (y_test == 1)].sum())

    report = {
        "threshold": threshold,
        "test_set_size": int(len(y_test)),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "false_positive_cost_inr": false_positive_cost,
        "revenue_recovered_inr": recovered_by_model,
        "revenue_recoverable_inr": recovered_if_perfect,
        "recovery_rate": round(recovered_by_model / max(recovered_if_perfect, 1), 3),
    }
    return report, scorer


if __name__ == "__main__":
    report, _ = evaluate()
    print(json.dumps(report, indent=2))
