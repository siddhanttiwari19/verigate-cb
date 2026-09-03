from app.evidence_integrity import check_integrity


def test_consistent_evidence_passes():
    evidence = {
        "delivery_confirmation": True,
        "signature_matches_cardholder": True,
        "prior_clean_order_count": 3,
        "refund_already_issued": False,
        "device_fingerprint_reused": False,
    }
    result = check_integrity(evidence)
    assert result.is_consistent
    assert result.flags == []


def test_signature_match_without_delivery_is_flagged():
    evidence = {"signature_matches_cardholder": True, "delivery_confirmation": False}
    result = check_integrity(evidence)
    assert not result.is_consistent
    assert "signature_match_without_delivery_confirmation" in result.flags


def test_implausible_order_count_is_flagged():
    evidence = {"prior_clean_order_count": -5}
    result = check_integrity(evidence)
    assert not result.is_consistent
    assert "implausible_prior_order_count" in result.flags


def test_device_reuse_with_first_time_match_is_flagged():
    evidence = {
        "device_fingerprint_reused": True,
        "signature_matches_cardholder": True,
        "prior_clean_order_count": 0,
    }
    result = check_integrity(evidence)
    assert not result.is_consistent
    assert "device_reuse_with_first_time_signature_match" in result.flags
