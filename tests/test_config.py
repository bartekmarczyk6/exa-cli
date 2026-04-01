"""Config precedence tests: override > env > file > None."""
import json
import pytest
import exa_cli.config as config_module
from exa_cli.config import get_api_key


def test_api_key_override_takes_precedence(monkeypatch, tmp_path):
    monkeypatch.setenv("EXA_API_KEY", "env-key")
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"api_key": "file-key"}))
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)

    result = get_api_key("override-key")
    assert result == "override-key"


def test_env_var_over_config_file(monkeypatch, tmp_path):
    monkeypatch.setenv("EXA_API_KEY", "env-key")
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"api_key": "file-key"}))
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)

    result = get_api_key()
    assert result == "env-key"


def test_config_file_fallback(monkeypatch, tmp_path):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"api_key": "file-key"}))
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)

    result = get_api_key()
    assert result == "file-key"


def test_no_key_returns_none(monkeypatch, tmp_path):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    config_file = tmp_path / "config.json"
    # File does not exist
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)

    result = get_api_key()
    assert result is None
