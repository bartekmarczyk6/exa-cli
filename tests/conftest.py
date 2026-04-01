import pytest
import respx
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner(mix_stderr=False)


@pytest.fixture
def api_key_env(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key")
