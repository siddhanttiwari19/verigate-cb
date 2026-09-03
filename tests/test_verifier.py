from app.verifier import verify


def test_verifier_approves_fully_supported_claims():
    evidence = {
        "delivery_confirmation": True,
        "signature_matches_cardholder": True,
        "ip_matches_billing_country": True,
        "prior_clean_order_count": 5,
        "refund_already_issued": False,
    }
    result = verify(["DELIVERY_CONFIRMED", "SIGNATURE_MATCH", "REPEAT_CUSTOMER"], evidence)
    assert result.approved
    assert result.rejected_claims == []


def test_verifier_rejects_unsupported_signature_claim():
    evidence = {
        "delivery_confirmation": True,
        "signature_matches_cardholder": False,  # not actually true
    }
    result = verify(["SIGNATURE_MATCH"], evidence)
    assert not result.approved
    assert "SIGNATURE_MATCH" in result.rejected_claims


def test_verifier_rejects_unknown_claim_tag():
    result = verify(["MADE_UP_CLAIM"], {})
    assert not result.approved
    assert "MADE_UP_CLAIM" in result.rejected_claims


def test_verifier_rejects_refund_claim_when_refund_was_issued():
    evidence = {"refund_already_issued": True}
    result = verify(["NO_PRIOR_REFUND"], evidence)
    assert not result.approved


def test_verifier_approves_empty_claim_list():
    result = verify([], {})
    assert result.approved
