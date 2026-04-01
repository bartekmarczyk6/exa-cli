import pytest
import respx
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def api_key_env(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key")
