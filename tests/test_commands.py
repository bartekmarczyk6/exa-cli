"""CLI integration tests using CliRunner and respx to mock HTTP."""
import json
import pytest
import httpx
import respx
from click.testing import CliRunner
from exa_cli.main import cli

BASE = "https://api.exa.ai"
SEARCH_RESULT = {"results": [{"title": "T", "url": "http://x.com", "id": "1"}]}
EMPTY_RESULTS = {"results": []}


# ---------------------------------------------------------------------------
# Search tests
# ---------------------------------------------------------------------------

@respx.mock
def test_search_basic():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(200, json=SEARCH_RESULT))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "search", "test"])
    assert result.exit_code == 0, result.output


@respx.mock
def test_search_with_domains():
    captured = {}

    def capture(request, route):
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=SEARCH_RESULT)

    respx.post(f"{BASE}/search").mock(side_effect=capture)
    runner = CliRunner()
    runner.invoke(cli, ["--api-key", "test-key", "search", "test", "--include-domains", "ex.com,y.com"])
    assert captured["body"]["includeDomains"] == ["ex.com", "y.com"]


@respx.mock
def test_search_with_contents_flags():
    captured = {}

    def capture(request, route):
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=SEARCH_RESULT)

    respx.post(f"{BASE}/search").mock(side_effect=capture)
    runner = CliRunner()
    runner.invoke(cli, ["--api-key", "test-key", "search", "test", "--text", "--highlights", "--summary"])
    body = captured["body"]
    assert "contents" in body
    assert "text" in body["contents"]
    assert "highlights" in body["contents"]
    assert "summary" in body["contents"]


@respx.mock
def test_search_deep_with_schema():
    captured = {}

    def capture(request, route):
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=SEARCH_RESULT)

    respx.post(f"{BASE}/search").mock(side_effect=capture)
    runner = CliRunner()
    runner.invoke(cli, [
        "--api-key", "test-key", "search", "test",
        "--type", "deep",
        "--output-schema", '{"type": "object"}'
    ])
    assert captured["body"].get("outputSchema") == {"type": "object"}


# ---------------------------------------------------------------------------
# Find-similar tests
# ---------------------------------------------------------------------------

@respx.mock
def test_find_similar_basic():
    respx.post(f"{BASE}/findSimilar").mock(return_value=httpx.Response(200, json=SEARCH_RESULT))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "find-similar", "http://example.com"])
    assert result.exit_code == 0, result.output


@respx.mock
def test_find_similar_with_filters():
    captured = {}

    def capture(request, route):
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json=SEARCH_RESULT)

    respx.post(f"{BASE}/findSimilar").mock(side_effect=capture)
    runner = CliRunner()
    runner.invoke(cli, [
        "--api-key", "test-key", "find-similar", "http://example.com",
        "--start-published-date", "2024-01-01",
        "--include-domains", "example.com"
    ])
    body = captured["body"]
    assert body["startPublishedDate"] == "2024-01-01"
    assert body["includeDomains"] == ["example.com"]


# ---------------------------------------------------------------------------
# Contents tests
# ---------------------------------------------------------------------------

@respx.mock
def test_contents_basic():
    captured = {}

    def capture(request, route):
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"results": []})

    respx.post(f"{BASE}/contents").mock(side_effect=capture)
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "contents", "http://a.com", "http://b.com"])
    assert result.exit_code == 0, result.output
    assert captured["body"]["urls"] == ["http://a.com", "http://b.com"]


# ---------------------------------------------------------------------------
# Answer tests
# ---------------------------------------------------------------------------

@respx.mock
def test_answer_basic():
    respx.post(f"{BASE}/answer").mock(return_value=httpx.Response(200, json={"answer": "A search engine", "citations": []}))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "answer", "what is exa"])
    assert result.exit_code == 0, result.output


# ---------------------------------------------------------------------------
# Research tests
# ---------------------------------------------------------------------------

@respx.mock
def test_research_create():
    respx.post(f"{BASE}/research/v0/tasks").mock(
        return_value=httpx.Response(200, json={"id": "task-1", "status": "running"})
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "research", "create", "analyze AI"])
    assert result.exit_code == 0, result.output


@respx.mock
def test_research_create_poll():
    """Test poll flow displays research content from the 'data' key (actual API response shape)."""
    import unittest.mock as mock

    respx.post(f"{BASE}/research/v0/tasks").mock(
        return_value=httpx.Response(200, json={"id": "task-1", "status": "running"})
    )
    respx.get(f"{BASE}/research/v0/tasks/task-1").mock(
        return_value=httpx.Response(200, json={"id": "task-1", "status": "completed", "data": {"summary": "done"}})
    )
    runner = CliRunner()
    with mock.patch("time.sleep"):
        result = runner.invoke(cli, ["--api-key", "test-key", "research", "create", "analyze AI", "--poll"])
    assert result.exit_code == 0, result.output
    assert "output:" in result.output  # TOON format


@respx.mock
def test_research_get():
    respx.get(f"{BASE}/research/v0/tasks/task-1").mock(
        return_value=httpx.Response(200, json={"id": "task-1", "status": "completed", "data": {"summary": "done"}})
    )
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "research", "get", "task-1"])
    assert result.exit_code == 0, result.output


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------

def test_no_api_key(monkeypatch, tmp_path):
    import exa_cli.config as config_module
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    # Point config file to a non-existent path so no stored key is found
    monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "test"])
    assert result.exit_code != 0
    assert "API key required" in result.output


@respx.mock
def test_401_error():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(401, json={"error": "Unauthorized"}))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "bad-key", "search", "test"])
    assert result.exit_code != 0
    assert "Invalid API key" in result.output


@respx.mock
def test_402_error():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(402, json={"error": "Payment required"}))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "search", "test"])
    assert result.exit_code != 0
    assert "Out of credits" in result.output


@respx.mock
def test_400_error():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(400, json={"error": "bad query", "tag": "VALIDATION"}))
    runner = CliRunner()
    result = runner.invoke(cli, ["--api-key", "test-key", "search", "test"])
    assert result.exit_code != 0
    assert "Validation Error" in result.output
