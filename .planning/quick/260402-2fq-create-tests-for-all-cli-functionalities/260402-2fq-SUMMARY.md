---
phase: quick
plan: 2fq
subsystem: tests
tags: [testing, bug-fix, cli, respx, pytest]
dependency_graph:
  requires: []
  provides: [test-suite, empty-response-fix]
  affects: [src/exa_cli/client.py, tests/]
tech_stack:
  added: [respx, pytest]
  patterns: [respx.mock decorator for httpx mocking, monkeypatch for env/config isolation]
key_files:
  created:
    - tests/conftest.py
    - tests/test_client.py
    - tests/test_commands.py
    - tests/test_config.py
  modified:
    - src/exa_cli/client.py
    - tests/test_search.py
    - tests/test_contents.py
decisions:
  - Used respx (native httpx mocker) instead of responses/httpretty since the client uses httpx
  - Monkeypatched config_module.CONFIG_FILE to isolate tests from real ~/.exa/config.json
  - Dropped CliRunner(mix_stderr=False) — not supported in Click 8.3.1
metrics:
  duration: ~15 minutes
  completed: 2026-04-02
  tasks_completed: 2
  files_changed: 7
---

# Phase quick Plan 2fq: Create Tests for All CLI Functionalities Summary

**One-liner:** Fixed JSONDecodeError on empty API responses and added 30 pytest tests covering all CLI commands, error codes, flag mapping, and config precedence using respx to mock httpx.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Fix client.py empty response bug and add client tests | a9863a2 | src/exa_cli/client.py, tests/conftest.py, tests/test_client.py |
| 2 | Comprehensive CLI command tests and config tests | 7428101 | tests/test_commands.py, tests/test_config.py, tests/test_search.py, tests/test_contents.py |

## What Was Built

### Bug Fix: Empty Response Handling

`client.py _request` previously called `response.json()` unconditionally, causing JSONDecodeError when the API returned a 204 or empty body (affecting `research create --poll`). Fixed by checking `response.status_code == 204 or not response.content` before parsing JSON.

### Test Suite (30 tests)

- **test_client.py** (9 tests): ExaClient unit tests — success, empty body, 204, retries on 429/5xx, 401/402/400 error codes
- **test_commands.py** (15 tests): CLI integration tests for all commands (search, find-similar, contents, answer, research create/poll/get) plus error handling
- **test_config.py** (4 tests): Config precedence (override > env > file > None)
- **test_search.py** / **test_contents.py** (2 tests): No-API-key guard tests

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CliRunner mix_stderr not supported in Click 8.3.1**
- **Found during:** Task 2 execution
- **Issue:** `CliRunner(mix_stderr=False)` raised TypeError in Click 8.3.1
- **Fix:** Changed to plain `CliRunner()` in all test files and conftest.py
- **Files modified:** tests/conftest.py, tests/test_commands.py

**2. [Rule 1 - Bug] Config file isolation needed for no-api-key tests**
- **Found during:** Task 2 execution
- **Issue:** Tests asserting "API key required" passed exit_code 0 because a real `~/.exa/config.json` with an API key existed on the machine
- **Fix:** Added `monkeypatch.setattr(config_module, "CONFIG_FILE", tmp_path / "config.json")` to all no-api-key tests to isolate from the real config file
- **Files modified:** tests/test_search.py, tests/test_contents.py, tests/test_commands.py

## Self-Check: PASSED

Files exist:
- src/exa_cli/client.py - FOUND
- tests/conftest.py - FOUND
- tests/test_client.py - FOUND
- tests/test_commands.py - FOUND
- tests/test_config.py - FOUND

Commits exist:
- a9863a2 - FOUND
- 7428101 - FOUND

All 30 tests pass: `python -m pytest tests/ -v` - CONFIRMED
