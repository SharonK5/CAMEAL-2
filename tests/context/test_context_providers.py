"""
===============================================================================
Tests for context providers: YamlContextProvider, CachedContextProvider, ContextLoader
===============================================================================
"""

import time
import pytest
from pathlib import Path
from unittest.mock import patch

from context import (
    GovernanceContext,
    YamlContextProvider,
    CachedContextProvider,
    ContextLoader,
    ContextProvider,
    InstitutionalContext,
    JurisdictionalContext,
    SpatialContext,
    TemporalContext,
    OperationalContext,
)


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def valid_yaml_content() -> str:
    """A valid YAML representation of a GovernanceContext."""
    return """
institutional:
  identifier: "test-org"
  name: "Test Ministry"
  institution_type: "Ministry"
  sector: "Agriculture"
  level: "National"
  parent: null
  authority: "Strategic"
  ownership: "Public"
  mandates:
    - "Policy"
    - "Food Security"
  responsibilities:
    - "Monitoring"
    - "Evaluation"

jurisdictional:
  authority: "Kenya"

spatial:
  country: "Kenya"
  region: "Nairobi"

temporal:
  fiscal_year: "2026"

operational:
  environment: "production"
  execution_mode: "async"
  sensitivity: "medium"

metadata:
  source: "test"
  version: 1
"""


@pytest.fixture
def yaml_dir(tmp_path: Path, valid_yaml_content: str) -> Path:
    """A temporary directory containing one valid YAML file."""
    dir_path = tmp_path / "contexts"
    dir_path.mkdir()
    (dir_path / "test-org.yaml").write_text(valid_yaml_content)
    return dir_path


@pytest.fixture
def yaml_provider(yaml_dir: Path) -> YamlContextProvider:
    return YamlContextProvider(yaml_dir)


@pytest.fixture
def cached_provider(yaml_provider: YamlContextProvider) -> CachedContextProvider:
    return CachedContextProvider(yaml_provider, ttl_seconds=60)


@pytest.fixture
def loader_with_cache(cached_provider: CachedContextProvider) -> ContextLoader:
    return ContextLoader([cached_provider])


# -----------------------------------------------------------------------------
# Tests for YamlContextProvider
# -----------------------------------------------------------------------------

def test_yaml_provider_loads_all(yaml_provider: YamlContextProvider):
    contexts = yaml_provider.load_all()
    assert len(contexts) == 1
    ctx = contexts[0]
    assert isinstance(ctx, GovernanceContext)
    assert ctx.institutional.identifier == "test-org"
    assert ctx.institutional.name == "Test Ministry"
    assert ctx.jurisdictional.authority == "Kenya"
    assert ctx.spatial.country == "Kenya"
    assert ctx.operational.sensitivity == "medium"
    assert dict(ctx.metadata) == {"source": "test", "version": 1}


def test_yaml_provider_get_by_identifier(yaml_provider: YamlContextProvider):
    ctx = yaml_provider.get("test-org")
    assert ctx is not None
    assert ctx.institutional.identifier == "test-org"

    # Unknown identifier returns None
    assert yaml_provider.get("unknown") is None


def test_yaml_provider_list_identifiers(yaml_provider: YamlContextProvider):
    identifiers = yaml_provider.list_identifiers()
    assert identifiers == ("test-org",)


def test_yaml_provider_handles_empty_yaml(tmp_path: Path):
    dir_path = tmp_path / "empty"
    dir_path.mkdir()
    (dir_path / "empty.yaml").write_text("")
    provider = YamlContextProvider(dir_path)
    # Should warn, but not raise, and return empty
    with pytest.warns(UserWarning, match="Empty YAML file"):
        contexts = provider.load_all()
    assert contexts == ()


def test_yaml_provider_handles_missing_directory():
    provider = YamlContextProvider(Path("/nonexistent"))
    provider = YamlContextProvider(Path("/nonexistent"))
    with pytest.raises(FileNotFoundError, match="not found"):
        provider.load_all()
        provider.load_all()

def test_yaml_provider_duplicate_identifier(tmp_path: Path, valid_yaml_content: str):
    """If two files define the same identifier, the last one wins with a warning."""
    dir_path = tmp_path / "dups"
    dir_path.mkdir()
    (dir_path / "first.yaml").write_text(valid_yaml_content)
    # Write second file with same identifier but different name
    second = valid_yaml_content.replace("Test Ministry", "Duplicate Ministry")
    (dir_path / "second.yaml").write_text(second)
    provider = YamlContextProvider(dir_path)
    with pytest.warns(UserWarning, match="Duplicate identifier 'test-org'"):
        contexts = provider.load_all()
    # The second one overwrote the first
    assert len(contexts) == 1
    ctx = contexts[0]
    assert ctx.institutional.name == "Duplicate Ministry"


# -----------------------------------------------------------------------------
# Tests for CachedContextProvider
# -----------------------------------------------------------------------------

def test_cached_provider_caches_get(cached_provider: CachedContextProvider, yaml_provider: YamlContextProvider):
    # First call hits the underlying provider
    ctx1 = cached_provider.get("test-org")
    # Second call should hit cache (no expensive load)
    ctx2 = cached_provider.get("test-org")
    assert ctx1 is ctx2  # same object (cache returns the same instance)

    # Test that the underlying provider is not called twice
    original_get = yaml_provider.get
    call_count = 0

    def mock_get(identifier):
        nonlocal call_count
        call_count += 1
        return original_get(identifier)

    with patch.object(yaml_provider, 'get', side_effect=mock_get):
        cached_provider.get("test-org")  # cache hit, no call
        assert call_count == 0


def test_cached_provider_ttl_expiry():
    """After TTL, the cache should refresh from the underlying provider."""
    provider = YamlContextProvider(Path("tests/data/contexts"))  # dummy path; we'll mock
    cache = CachedContextProvider(provider, ttl_seconds=1)

    # Mock provider to return a new object each time
    mock_context = GovernanceContext(
        institutional=InstitutionalContext(identifier="test"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )
    provider.get = lambda x: mock_context

    # First call stores in cache
    ctx1 = cache.get("test")
    assert ctx1 is mock_context

    # Wait for TTL to expire
    time.sleep(1.1)

    # Second call should call provider again
    new_mock = GovernanceContext(
        institutional=InstitutionalContext(identifier="test", name="New"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )
    provider.get = lambda x: new_mock
    ctx2 = cache.get("test")
    assert ctx2 is new_mock
    assert ctx2 is not ctx1


def test_cached_provider_load_all(cached_provider: CachedContextProvider):
    contexts = cached_provider.load_all()
    assert len(contexts) == 1
    # Second call should return the same tuple (cached)
    contexts2 = cached_provider.load_all()
    assert contexts is contexts2  # same object


# -----------------------------------------------------------------------------
# Tests for ContextLoader
# -----------------------------------------------------------------------------

def test_loader_single_provider(loader_with_cache: ContextLoader):
    ctx = loader_with_cache.get("test-org")
    assert ctx is not None
    assert ctx.institutional.identifier == "test-org"


def test_loader_unknown(loader_with_cache: ContextLoader):
    assert loader_with_cache.get("unknown") is None


def test_loader_chain():
    """Loader tries providers in order; returns first match."""
    # Provider A returns a context for "id1"
    provider_a = FakeProvider({"id1": GovernanceContext(
        institutional=InstitutionalContext(identifier="id1", name="A"),
        jurisdictional=JurisdictionalContext(),
        spatial=SpatialContext(),
        temporal=TemporalContext(),
        operational=OperationalContext(),
    )})
    # Provider B also has "id1" (different) and "id2"
    provider_b = FakeProvider({
        "id1": GovernanceContext(
            institutional=InstitutionalContext(identifier="id1", name="B"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
        "id2": GovernanceContext(
            institutional=InstitutionalContext(identifier="id2", name="B2"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
    })

    loader = ContextLoader([provider_a, provider_b])

    ctx = loader.get("id1")
    assert ctx.institutional.name == "A"  # first provider wins
    ctx2 = loader.get("id2")
    assert ctx2.institutional.name == "B2"  # from second provider


def test_loader_deduplicates_load_all():
    """When load_all() is called, contexts with same identifier are deduplicated (first wins)."""
    provider_a = FakeProvider({
        "id1": GovernanceContext(
            institutional=InstitutionalContext(identifier="id1", name="A"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
        "id2": GovernanceContext(
            institutional=InstitutionalContext(identifier="id2", name="A2"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
    })
    provider_b = FakeProvider({
        "id1": GovernanceContext(
            institutional=InstitutionalContext(identifier="id1", name="B"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
        "id3": GovernanceContext(
            institutional=InstitutionalContext(identifier="id3", name="B3"),
            jurisdictional=JurisdictionalContext(),
            spatial=SpatialContext(),
            temporal=TemporalContext(),
            operational=OperationalContext(),
        ),
    })
    loader = ContextLoader([provider_a, provider_b])
    all_contexts = loader.load_all()
    # Should have id1 (from A), id2 (from A), id3 (from B) – id1 deduplicated
    identifiers = [ctx.institutional.identifier for ctx in all_contexts]
    assert set(identifiers) == {"id1", "id2", "id3"}
    # id1 should be from provider A (first)
    id1_ctx = next(ctx for ctx in all_contexts if ctx.institutional.identifier == "id1")
    assert id1_ctx.institutional.name == "A"


# -----------------------------------------------------------------------------
# Helper class for testing
# -----------------------------------------------------------------------------

class FakeProvider(ContextProvider):
    """Simple in-memory provider for testing chains."""
    def __init__(self, contexts: dict[str, GovernanceContext]):
        self._contexts = contexts

    def get(self, identifier: str) -> GovernanceContext | None:
        return self._contexts.get(identifier)

    def list_identifiers(self):
        return tuple(self._contexts.keys())

    def load_all(self):
        return tuple(self._contexts.values())
