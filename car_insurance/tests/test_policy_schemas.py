import pytest
from pydantic import ValidationError

from app.api.schemas.policy_schemas import PolicyCreate


def test_policy_create_accepts_valid_data():
    policy = PolicyCreate(
        provider="Groupama",
        start_date="2031-01-01",
        end_date="2031-12-31",
        paid_amount=1200.00,
    )

    assert policy.provider == "Groupama"
    assert str(policy.start_date) == "2031-01-01"
    assert str(policy.end_date) == "2031-12-31"
    assert policy.paid_amount == 1200.00


def test_policy_create_rejects_short_provider():
    with pytest.raises(ValidationError):
        PolicyCreate(
            provider="A",
            start_date="2031-01-01",
            end_date="2031-12-31",
            paid_amount=1200.00,
        )


def test_policy_create_rejects_invalid_provider_characters():
    with pytest.raises(ValidationError):
        PolicyCreate(
            provider="Groupama!",
            start_date="2031-01-01",
            end_date="2031-12-31",
            paid_amount=1200.00,
        )


def test_policy_create_rejects_end_date_before_start_date():
    with pytest.raises(ValidationError):
        PolicyCreate(
            provider="Groupama",
            start_date="2031-12-31",
            end_date="2031-01-01",
            paid_amount=1200.00,
        )


def test_policy_create_rejects_zero_paid_amount():
    with pytest.raises(ValidationError):
        PolicyCreate(
            provider="Groupama",
            start_date="2031-01-01",
            end_date="2031-12-31",
            paid_amount=0,
        )


def test_policy_create_rejects_too_large_paid_amount():
    with pytest.raises(ValidationError):
        PolicyCreate(
            provider="Groupama",
            start_date="2031-01-01",
            end_date="2031-12-31",
            paid_amount=1_000_001,
        )