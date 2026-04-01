import pytest
import httpx
import respx
import click
from exa_cli.client import ExaClient

BASE = "https://api.exa.ai"


@respx.mock
def test_post_success():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(200, json={"results": []}))
    client = ExaClient("test-key")
    result = client.post("/search", json={"query": "test"})
    assert result == {"results": []}


@respx.mock
def test_get_success():
    respx.get(f"{BASE}/research/v0/tasks/abc").mock(return_value=httpx.Response(200, json={"id": "abc", "status": "running"}))
    client = ExaClient("test-key")
    result = client.get("/research/v0/tasks/abc")
    assert result["id"] == "abc"


@respx.mock
def test_empty_response_returns_dict():
    respx.post(f"{BASE}/research/v0/tasks").mock(return_value=httpx.Response(204, content=b""))
    client = ExaClient("test-key")
    result = client.post("/research/v0/tasks", json={"instructions": "test"})
    assert result == {}


@respx.mock
def test_empty_body_non_204_returns_dict():
    respx.post(f"{BASE}/research/v0/tasks").mock(return_value=httpx.Response(200, content=b""))
    client = ExaClient("test-key")
    result = client.post("/research/v0/tasks", json={"instructions": "test"})
    assert result == {}


@respx.mock
def test_retry_on_429():
    route = respx.post(f"{BASE}/search")
    route.side_effect = [
        httpx.Response(429, json={"error": "rate limited"}),
        httpx.Response(200, json={"results": []}),
    ]
    client = ExaClient("test-key")
    # Patch sleep to avoid waiting
    import unittest.mock as mock
    with mock.patch("time.sleep"):
        result = client.post("/search", json={"query": "test"})
    assert result == {"results": []}


@respx.mock
def test_retry_on_5xx():
    route = respx.post(f"{BASE}/search")
    route.side_effect = [
        httpx.Response(500, json={"error": "server error"}),
        httpx.Response(200, json={"results": []}),
    ]
    client = ExaClient("test-key")
    import unittest.mock as mock
    with mock.patch("time.sleep"):
        result = client.post("/search", json={"query": "test"})
    assert result == {"results": []}


@respx.mock
def test_401_raises_abort():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(401, json={"error": "Unauthorized"}))
    client = ExaClient("test-key")
    with pytest.raises(click.Abort):
        client.post("/search", json={"query": "test"})


@respx.mock
def test_402_raises_abort():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(402, json={"error": "Payment required"}))
    client = ExaClient("test-key")
    with pytest.raises(click.Abort):
        client.post("/search", json={"query": "test"})


@respx.mock
def test_400_raises_abort():
    respx.post(f"{BASE}/search").mock(return_value=httpx.Response(400, json={"error": "bad query", "tag": "VALIDATION"}))
    client = ExaClient("test-key")
    with pytest.raises(click.Abort):
        client.post("/search", json={"query": "test"})
