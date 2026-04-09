import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from exa_cli.main import cli


def test_search_no_api_key(monkeypatch, tmp_path):
    import exa_cli.config as config_module
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "test query"])
    assert result.exit_code != 0
    assert "API key required" in result.output


def test_search_default_output_is_toon(monkeypatch, tmp_path):
    """Default output format should be toon, not table."""
    import exa_cli.config as config_module
    monkeypatch.setenv("EXA_API_KEY", "test-key")
    monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")

    mock_data = {"results": [{"title": "Foo", "url": "https://foo.com", "score": 0.9}]}

    with patch("exa_cli.commands.search.ExaClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.post.return_value = mock_data
        mock_client_cls.return_value = mock_client

        runner = CliRunner()
        result = runner.invoke(cli, ["search", "test query"])

    assert result.exit_code == 0
    assert "results[1]" in result.output  # TOON header


def test_search_fields_flag(monkeypatch, tmp_path):
    """--fields should restrict TOON output columns."""
    import exa_cli.config as config_module
    monkeypatch.setenv("EXA_API_KEY", "test-key")
    monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")

    mock_data = {"results": [
        {"title": "Foo", "url": "https://foo.com", "score": 0.9, "publishedDate": "2024-01-01T00:00:00Z"}
    ]}

    with patch("exa_cli.commands.search.ExaClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.post.return_value = mock_data
        mock_client_cls.return_value = mock_client

        runner = CliRunner()
        result = runner.invoke(cli, ["search", "test query", "--fields", "title,url"])

    assert result.exit_code == 0
    assert "{title,url}" in result.output
    assert "0.9" not in result.output  # score excluded
