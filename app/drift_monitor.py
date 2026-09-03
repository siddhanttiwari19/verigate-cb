"""
Feature 4 — Drift Monitor.

A model silently getting worse because the real world changed (new fraud
pattern, new checkout flow, seasonal shift) is one of the most common
ways ML systems fail in production — and the failure is invisible unless
something is watching for it. This tracks a rolling window of live
winnability scores and flags when the distribution shifts meaningfully
from what the model saw during training.

On a flag, the orchestrator should widen the auto-submit threshold
(be more conservative) until a human confirms whether retraining is
needed — that wiring lives in orchestrator.py.
"""
from collections import deque
from dataclasses import dataclass

from app.config import settings


@dataclass
class DriftStatus:
    drifted: bool
    live_mean: float
    baseline_mean: float
    std_devs_from_baseline: float


class DriftMonitor:
    def __init__(self, baseline_mean: float, baseline_std: float):
        self.baseline_mean = baseline_mean
        self.baseline_std = max(baseline_std, 1e-6)  # avoid div-by-zero on degenerate baselines
        self.window: deque = deque(maxlen=settings.drift_check_window)

    def record(self, probability: float) -> DriftStatus:
        self.window.append(probability)
        return self.check()

    def check(self) -> DriftStatus:
        if len(self.window) < settings.drift_check_window:
            # Not enough live data yet to make a statistically meaningful call.
            return DriftStatus(
                False, live_mean=0.0, baseline_mean=self.baseline_mean, std_devs_from_baseline=0.0
            )

        live_mean = sum(self.window) / len(self.window)
        std_devs = abs(live_mean - self.baseline_mean) / self.baseline_std
        drifted = std_devs >= settings.drift_alert_std_devs

        return DriftStatus(
            drifted=drifted,
            live_mean=round(live_mean, 3),
            baseline_mean=round(self.baseline_mean, 3),
            std_devs_from_baseline=round(std_devs, 2),
        )
