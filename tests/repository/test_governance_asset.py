import pytest

from repository.governance_asset import GovernanceAsset


class DummyAsset(GovernanceAsset):
    pass


def test_identifier():

    asset = DummyAsset(
        identifier="policy-001",
        name="Climate Policy",
        asset_type="policy",
    )

    assert asset.identifier == "policy-001"


def test_name():

    asset = DummyAsset(
        identifier="1",
        name="Test",
        asset_type="policy",
    )

    assert asset.name == "Test"


def test_asset_type():

    asset = DummyAsset(
        identifier="1",
        name="Test",
        asset_type="dataset",
    )

    assert asset.asset_type == "dataset"


def test_metadata():

    asset = DummyAsset(
        identifier="1",
        name="Test",
        asset_type="policy",
        metadata={
            "country": "Kenya",
        },
    )

    assert asset.get("country") == "Kenya"


def test_contains():

    asset = DummyAsset(
        identifier="1",
        name="Test",
        asset_type="policy",
        metadata={
            "country": "Kenya",
        },
    )

    assert asset.contains("country")


def test_missing_metadata():

    asset = DummyAsset(
        identifier="1",
        name="Test",
        asset_type="policy",
    )

    assert asset.get("missing") is None
