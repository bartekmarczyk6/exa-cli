import pytest
from exa_cli.formatters import truncate, toon_row, print_toon_results
from io import StringIO
import sys

def test_truncate_short_string():
    assert truncate("hello", 100) == "hello"

def test_truncate_long_string():
    result = truncate("x" * 1000, 50)
    assert result.startswith("x" * 50)
    assert "truncated" in result
    assert "1000" in result

def test_truncate_none():
    assert truncate(None, 100) == ""

def test_toon_row_basic():
    result = toon_row(["Fix auth", "https://x.com", "0.921"])
    assert result == "  Fix auth,https://x.com,0.921"

def test_print_toon_results_empty(capsys):
    from exa_cli.formatters import print_toon_results
    print_toon_results([], query="test")
    out = capsys.readouterr().out
    assert "0" in out
    assert "test" in out

def test_print_toon_results_basic(capsys):
    results = [
        {"title": "Foo", "url": "https://foo.com", "score": 0.9},
        {"title": "Bar", "url": "https://bar.com", "score": 0.8},
    ]
    print_toon_results(results)
    out = capsys.readouterr().out
    assert "results[2]" in out
    assert "Foo,https://foo.com,0.900" in out
    assert "Bar,https://bar.com,0.800" in out

def test_print_toon_results_fields(capsys):
    results = [{"title": "Foo", "url": "https://foo.com", "score": 0.9, "publishedDate": "2024-01-01"}]
    print_toon_results(results, fields=["title", "url"])
    out = capsys.readouterr().out
    assert "{title,url}" in out
    assert "2024" not in out

def test_print_toon_results_with_text_truncated(capsys):
    results = [{"title": "Foo", "url": "https://foo.com", "score": 0.9, "text": "a" * 2000}]
    print_toon_results(results, show_text=True)
    out = capsys.readouterr().out
    assert "truncated" in out
    assert "2000" in out


def test_print_toon_answer_basic(capsys):
    from exa_cli.formatters import print_toon_answer
    data = {
        "answer": "The sky is blue.",
        "citations": [
            {"title": "Sky article", "url": "https://sky.com"},
        ]
    }
    print_toon_answer(data)
    out = capsys.readouterr().out
    assert "answer:" in out
    assert "The sky is blue." in out
    assert "citations[1]" in out
    assert "Sky article,https://sky.com" in out

def test_print_toon_answer_truncates_long_answer(capsys):
    from exa_cli.formatters import print_toon_answer
    data = {"answer": "x" * 2000, "citations": []}
    print_toon_answer(data)
    out = capsys.readouterr().out
    assert "truncated" in out

def test_print_toon_research_pending(capsys):
    from exa_cli.formatters import print_toon_research
    data = {"id": "abc123", "status": "pending"}
    print_toon_research(data)
    out = capsys.readouterr().out
    assert "task:" in out
    assert "abc123" in out
    assert "pending" in out

def test_print_toon_research_completed_truncates(capsys):
    from exa_cli.formatters import print_toon_research
    data = {"id": "abc123", "status": "completed", "data": {"result": "x" * 2000}}
    print_toon_research(data)
    out = capsys.readouterr().out
    assert "truncated" in out
    assert "abc123" in out


def test_print_error_basic(capsys):
    from exa_cli.formatters import print_error
    print_error("--title is required", fix="exa search --help")
    out = capsys.readouterr().out
    assert "error:" in out
    assert "--title is required" in out
    assert "exa search --help" in out

def test_output_results_toon_search(capsys):
    from exa_cli.formatters import output_results
    data = {"results": [{"title": "Foo", "url": "https://foo.com", "score": 0.9}]}
    output_results(data, "toon", command_type="search")
    out = capsys.readouterr().out
    assert "results[1]" in out

def test_output_results_toon_answer(capsys):
    from exa_cli.formatters import output_results
    data = {"answer": "42", "citations": []}
    output_results(data, "toon", command_type="answer")
    out = capsys.readouterr().out
    assert "answer:" in out
