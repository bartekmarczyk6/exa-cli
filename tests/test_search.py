import pytest
from click.testing import CliRunner
from exa_cli.main import cli

def test_search_no_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "test query"])
    assert result.exit_code != 0
    assert "API key required" in result.output
