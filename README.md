<h1 align="center">
  exa-cli
</h1>

<p align="center">
  <b>Like <code>gh</code> for GitHub, but for the Exa Search API. Neural search in your terminal.</b>
</p>

<p align="center">
  <img src="https://via.placeholder.com/640x320.png?text=Add+a+GIF+of+your+CLI+here" alt="demo" width="640">
</p>

<p align="center">
  <a href="https://github.com/bartekmarczyk6/exa-cli/releases"><img src="https://img.shields.io/github/v/release/bartekmarczyk6/exa-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/bartekmarczyk6/exa-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/bartekmarczyk6/exa-cli/ci.yml?style=flat-square&label=tests" alt="Tests"></a>
  <a href="https://github.com/bartekmarczyk6/exa-cli/blob/main/LICENSE"><img src="https://img.shields.io/github/license/bartekmarczyk6/exa-cli?style=flat-square" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square" alt="Python 3.9+"></a>
</p>

---

A full-featured command-line interface for the [Exa Search API](https://exa.ai). Perform neural web searches, find similar pages, extract clean HTML contents, and run deep multi-step research — all from your terminal. Built for developers and AI agents who need programmatic access to the web without the browser.

## Install

### One-Line Install (macOS / Linux)
The recommended way to install `exa-cli` is via our one-line installer script, which safely installs the tool in an isolated environment using `pipx`.

```sh
curl -sSL https://raw.githubusercontent.com/bartekmarczyk6/exa-cli/main/install.sh | bash
```

### pipx (Cross-Platform)
If you already have [`pipx`](https://pipx.pypa.io/stable/) installed:

```sh
pipx install git+https://github.com/bartekmarczyk6/exa-cli.git
```

## Quick Start

```sh
# Authenticate
export EXA_API_KEY="your-api-key-here"
# Or use the login command
exa auth login

# Search the web using neural search
exa search "latest breakthroughs in quantum computing" --type neural -n 5

# Find similar pages to a given URL
exa find-similar "https://github.com" -n 3 --highlights

# Extract clean text from URLs
exa contents "https://example.com" --text --summary

# Ask a question and get an AI-generated answer
exa answer "Who won the Nobel Prize in Physics in 2023?" --text

# Start a deep research task
exa research create "Research the impact of quantum computing on cryptography" --poll
```

## Commands

| Group | Commands | Description |
|-------|----------|-------------|
| **auth** | `login` `status` | Authentication & diagnostics |
| **search** | `search` | Perform neural or keyword searches |
| **find** | `find-similar` | Discover pages similar to a URL |
| **content** | `contents` | Extract clean text/HTML from URLs |
| **answer** | `answer` | Ask questions and get cited answers |
| **research** | `create` `get` | Deep, multi-step asynchronous research |

## Features

### Neural Search
Search by meaning, not just keywords:
```sh
exa search "a great blog post about rust macros" --type neural
```

### Clean Content Extraction
Perfect for piping into LLMs. Get the text without the noise:
```sh
exa contents "https://example.com" --text > content.txt
```

### Smart Output
- **Terminal**: Cleanly formatted, readable output.
- **Pipe/Script**: Clean JSON or CSV for scripts and AI agents.
```sh
# JSON output for programmatic use
exa search "AI news" -o json | jq '.[].url'
```

### AI Answers
Get instant answers with citations from the web:
```sh
exa answer "How do I setup a Homebrew tap?"
```

## For AI Agents

This CLI is designed to be agent-friendly:
- **JSON output** when piped or requested via `-o json` — no parsing needed.
- **Direct content extraction** — perfect for agents reading web pages.
- **Research capabilities** — offload complex research tasks.

Install as an agent skill (Claude Code, Gemini CLI, etc.):
```sh
npx skills add bartekmarczyk6/exa-cli
```

## Configuration

```sh
# Set via environment variable (recommended for CI/Agents)
export EXA_API_KEY="your-api-key-here"

# Or configure interactively
exa auth login

# Check authentication status
exa auth status
```

## Local Development

1. Clone the repository:
   ```sh
   git clone https://github.com/bartekmarczyk6/exa-cli.git
   cd exa-cli
   ```
2. Create a virtual environment and install:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```
3. Run tests:
   ```sh
   pip install pytest
   pytest tests/
   ```

## Contributing

Issues and PRs welcome at [github.com/bartekmarczyk6/exa-cli](https://github.com/bartekmarczyk6/exa-cli).

## License

[MIT](LICENSE)
