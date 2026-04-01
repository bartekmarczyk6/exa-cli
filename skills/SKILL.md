---
name: exa-cli
description: How to use the Exa CLI tool for web search, content retrieval, similarity search, and deep research. Make sure to use this skill whenever the user asks to search the web, find recent news, get the contents of URLs, find similar websites, or perform deep research using the `exa` command.
---

# Exa CLI Usage Instructions

This skill provides instructions on how to use the `exa` CLI tool to interact with the Exa Search API. NEVER use the exa mcp, only exa-cli.

## Authentication
Before using the CLI, ensure the API key is set. You can do this by:
1. Setting the environment variable: `export EXA_API_KEY="your_api_key"`
2. Or using the auth command: `exa auth login`
3. Check status: `exa auth status`

## Core Commands

### 1. Search
Search the web using Exa's neural search capabilities.
`exa search "your search query" [OPTIONS]`

**Key Options:**
- `--type`: `auto` (default), `neural`, `fast`, `instant`, `deep`, `deep-reasoning`
- `-n, --num-results`: Number of results (default 10, max 100)
- `--text`: Include full text of the pages
- `--highlights`: Include highlights from the pages
- `-o, --output`: Output format (`table`, `json`, `csv`)

**Example:**
`exa search "latest breakthroughs in AI" --type neural -n 5 --text -o json`

### 2. Find Similar
Find web pages similar to a given URL.
`exa find-similar "https://example.com" [OPTIONS]`

**Example:**
`exa find-similar "https://github.com" -n 5 --highlights`

### 3. Contents
Retrieve the cleaned HTML/text contents of specific URLs.
`exa contents "https://url1.com" "https://url2.com" [OPTIONS]`

**Example:**
`exa contents "https://example.com" --text --summary`

### 4. Answer
Ask a question and get an AI-generated answer with citations.
`exa answer "your question" [OPTIONS]`

**Example:**
`exa answer "Who won the Nobel Prize in Physics in 2023?" --text`

### 5. Research
Perform deep, multi-step research tasks.
`exa research create "your research instructions" [OPTIONS]`

**Key Options:**
- `--poll`: Wait for the task to complete and print the results.

**Example:**
`exa research create "Research the impact of quantum computing on cryptography" --poll`

## Best Practices
- ALWAYS use `-o json` when you need to parse the output programmatically.
- If you need the actual content of the pages to answer a user's question, make sure to include the `--text` or `--highlights` flags in your `search` or `find-similar` commands.
- Use `--type deep` or `--type deep-reasoning` for complex queries that require extensive reasoning or multiple sub-queries.
