"""
Feature 2 — Amount-Scaled Dynamic Threshold.

A fixed confidence threshold treats a ₹500 dispute and a ₹40,000 dispute
identically. That's wrong: the cost of being confidently wrong scales
with the money at stake. This computes a per-dispute threshold instead
of a single global constant.
"""
from app.config import settings


def dynamic_threshold(amount_inr: int) -> float:
    """
    Returns the confidence bar this specific dispute must clear to
    auto-submit. High-value disputes need a stricter bar; the bonus
    scales smoothly rather than jumping at a hard cutoff, so there's
    no cliff-edge exploit at exactly the high-value boundary.
    """
    if amount_inr <= settings.high_value_amount_inr:
        return settings.base_auto_submit_threshold

    # Smooth scaling: every additional multiple of the high-value
    # threshold adds a fraction of the bonus, capped so the bar never
    # exceeds 0.99 (never require literal certainty).
    excess_ratio = amount_inr / settings.high_value_amount_inr
    scaled_bonus = min(settings.high_value_threshold_bonus * (excess_ratio - 1), 0.24)
    return min(settings.base_auto_submit_threshold + scaled_bonus, 0.99)
