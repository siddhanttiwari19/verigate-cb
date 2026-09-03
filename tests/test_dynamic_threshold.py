from app.config import settings
from app.dynamic_threshold import dynamic_threshold


def test_low_value_dispute_uses_base_threshold():
    assert dynamic_threshold(500) == settings.base_auto_submit_threshold


def test_high_value_dispute_requires_higher_threshold():
    low = dynamic_threshold(5000)
    high = dynamic_threshold(50000)
    assert high > low


def test_threshold_never_exceeds_cap():
    assert dynamic_threshold(10_000_000) <= 0.99
