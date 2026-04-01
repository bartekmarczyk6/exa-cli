import pytest
from click.testing import CliRunner
from exa_cli.main import cli


def test_search_no_api_key(monkeypatch, tmp_path):
    import exa_cli.config as config_module
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "test query"])
    assert result.exit_code != 0
    assert "API key required" in result.output
