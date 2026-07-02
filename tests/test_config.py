import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import get_api_keys


def test_get_api_keys_uses_standard_env_names(monkeypatch):
    monkeypatch.delenv("REPLIT_DEPLOYMENT", raising=False)
    monkeypatch.delenv("APP_MODE", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-test")
    monkeypatch.setenv("QDRANT_API_KEY", "qdrant-test")
    monkeypatch.setenv("QDRANT_URL", "https://example.test")
    monkeypatch.setenv("APP_PASSWORD", "app-password")

    keys = get_api_keys()

    assert keys == {
        "openai": "openai-test",
        "anthropic": "anthropic-test",
        "qdrant": "qdrant-test",
        "qdrant_url": "https://example.test",
        "app_password": "app-password",
        "app_mode": "live",
    }


def test_get_api_keys_ignores_legacy_env_names(monkeypatch):
    monkeypatch.delenv("REPLIT_DEPLOYMENT", raising=False)
    monkeypatch.delenv("APP_MODE", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("QDRANT_API_KEY", raising=False)
    monkeypatch.delenv("QDRANT_URL", raising=False)
    monkeypatch.delenv("APP_PASSWORD", raising=False)
    monkeypatch.delenv("APP_ACCESS_PASSWORD", raising=False)
    monkeypatch.setenv("OPENAI_KEY", "legacy-openai")
    monkeypatch.setenv("ANTHROPIC_KEY", "legacy-anthropic")
    monkeypatch.setenv("QDRANT_KEY", "legacy-qdrant")

    keys = get_api_keys()

    assert keys["openai"] is None
    assert keys["anthropic"] is None
    assert keys["qdrant"] is None


def test_get_api_keys_detects_mock_mode(monkeypatch):
    monkeypatch.delenv("REPLIT_DEPLOYMENT", raising=False)
    monkeypatch.setenv("APP_MODE", "mock")

    keys = get_api_keys()

    assert keys["app_mode"] == "mock"


def test_mock_mode_does_not_require_api_keys(monkeypatch):
    monkeypatch.setenv("REPLIT_DEPLOYMENT", "1")
    monkeypatch.setenv("APP_MODE", "mock")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("QDRANT_API_KEY", raising=False)
    monkeypatch.delenv("QDRANT_URL", raising=False)

    keys = get_api_keys()

    assert keys["app_mode"] == "mock"
    assert keys["openai"] is None
