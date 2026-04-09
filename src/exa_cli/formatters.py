import json
import csv
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def print_json(data):
    console.print_json(data=data)

def print_csv(results):
    if not results:
        return
    writer = csv.writer(sys.stdout)
    writer.writerow(["Title", "URL", "Published", "Score"])
    for res in results:
        title = res.get("title", "No Title")
        url = res.get("url", "")
        pub = res.get("publishedDate", "")[:10] if res.get("publishedDate") else ""
        score = f"{res.get('score', 0):.3f}"
        writer.writerow([title, url, pub, score])

def print_table_results(results, show_text=False, show_highlights=False):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", min_width=20)
    table.add_column("URL", overflow="fold")
    table.add_column("Published", justify="right")
    table.add_column("Score", justify="right")

    for i, res in enumerate(results):
        title = res.get("title", "No Title")
        url = res.get("url", "")
        pub = res.get("publishedDate", "")[:10] if res.get("publishedDate") else ""
        score = f"{res.get('score', 0):.3f}"
        table.add_row(str(i+1), title, url, pub, score)

    console.print(table)

    if show_text or show_highlights:
        for i, res in enumerate(results):
            console.print(f"\n[bold cyan]--- Result {i+1}: {res.get('title', 'No Title')} ---[/bold cyan]")
            if show_text and "text" in res:
                console.print(Panel(res["text"], title="Text", expand=False))
            if show_highlights and "highlights" in res:
                for h in res["highlights"]:
                    console.print(f"- {h}")
            if "summary" in res:
                console.print(Panel(res["summary"], title="Summary", expand=False))

def print_answer(data):
    answer = data.get("answer", "")
    console.print(Markdown(answer))
    citations = data.get("citations", [])
    if citations:
        console.print("\n[bold]Citations:[/bold]")
        for i, cit in enumerate(citations):
            console.print(f"[{i+1}] {cit.get('title', '')} - {cit.get('url', '')}")

def print_research_task(data):
    console.print(f"[bold]Task ID:[/bold] {data.get('id')}")
    console.print(f"[bold]Status:[/bold] {data.get('status')}")
    if data.get("status") == "completed":
        # The Exa Research API returns completed task content under "data";
        # fall back to "output" for backwards compatibility with older responses.
        result = data.get("data") or data.get("output")
        if result:
            console.print("\n[bold]Output:[/bold]")
            console.print_json(data=result)
        else:
            console.print("\n[bold]Output:[/bold] (no content returned)")

# ---------------------------------------------------------------------------
# TOON (Token-Oriented Object Notation) formatters
# ---------------------------------------------------------------------------

TOON_TRUNCATE_LIMIT = 500

def truncate(text, limit=TOON_TRUNCATE_LIMIT):
    """Truncate a string to limit chars; append hint with total size."""
    if text is None:
        return ""
    text = str(text)
    if len(text) <= limit:
        return text
    return f"{text[:limit]}\n    ... (truncated, {len(text)} chars total)"

def toon_row(values):
    """Format a list of values as a single indented TOON row."""
    return "  " + ",".join(str(v) for v in values)

DEFAULT_RESULT_FIELDS = ["title", "url", "score"]

def print_toon_results(results, fields=None, show_text=False,
                       show_highlights=False, query=None):
    """Emit results in TOON format."""
    if fields is None:
        fields = DEFAULT_RESULT_FIELDS

    if not results:
        q_hint = f' for "{query}"' if query else ""
        print(f"results: 0 found{q_hint}")
        return

    # Header
    print(f"results[{len(results)}]{{{','.join(fields)}}}:")

    for res in results:
        row = []
        for f in fields:
            if f == "score":
                row.append(f"{res.get('score', 0):.3f}")
            elif f == "publishedDate":
                v = res.get("publishedDate", "")
                row.append(v[:10] if v else "")
            else:
                row.append(res.get(f, ""))
        print(toon_row(row))

    # Long-form content blocks
    for i, res in enumerate(results):
        extras = []
        if show_text and "text" in res:
            extras.append(("text", res["text"]))
        if show_highlights and "highlights" in res:
            for h in res.get("highlights", []):
                extras.append(("highlight", h))
        if "summary" in res:
            extras.append(("summary", res["summary"]))

        if extras:
            print(f"\nresult[{i+1}] {res.get('title', '')}:")
            for label, content in extras:
                print(f"  {label}: {truncate(content)}")

    # Help hints
    hints = []
    if not show_text:
        hints.append("Run `exa search <query> --text` to include page text")
    if not show_highlights:
        hints.append("Run `exa search <query> --highlights` to include highlights")
    hints.append("Run `exa search <query> --output json` for raw JSON")

    if hints:
        print(f"\nhelp[{len(hints)}]:")
        for h in hints:
            print(f"  {h}")


def print_toon_answer(data):
    """Emit answer + citations in TOON format."""
    answer = data.get("answer", "")
    print(f"answer:\n  {truncate(answer)}")

    citations = data.get("citations", [])
    if citations:
        print(f"\ncitations[{len(citations)}]{{title,url}}:")
        for cit in citations:
            print(toon_row([cit.get("title", ""), cit.get("url", "")]))
    else:
        print("\ncitations: none")


def print_toon_research(data):
    """Emit research task status in TOON format."""
    task_id = data.get("id", "")
    status = data.get("status", "unknown")
    print(f"task:\n  id: {task_id}\n  status: {status}")

    if status == "completed":
        result = data.get("data") or data.get("output")
        if result:
            raw = json.dumps(result)
            print(f"\noutput:\n  {truncate(raw, limit=800)}")
            if len(raw) > 800:
                print(f"\nhelp[1]:\n  Run `exa research get {task_id} --output json` for full output")
        else:
            print("\noutput: (empty)")
    elif status == "failed":
        print(f"\nerror: task {task_id} failed")
    else:
        print(f"\nhelp[1]:\n  Run `exa research get {task_id}` to check status")


def print_error(message, fix=None):
    """Emit a structured error on stdout (not stderr) for agent readability."""
    print(f"error: {message}")
    if fix:
        print(f"help: {fix}")


def output_results(data, format_type, command_type="search", **kwargs):
    if format_type == "json":
        print_json(data)
        return

    if command_type in ("search", "find_similar", "contents"):
        results = data.get("results", [])
        if format_type == "csv":
            print_csv(results)
        elif format_type == "toon":
            print_toon_results(
                results,
                fields=kwargs.get("fields"),
                show_text=kwargs.get("show_text"),
                show_highlights=kwargs.get("show_highlights"),
                query=kwargs.get("query"),
            )
        else:
            print_table_results(results, show_text=kwargs.get("show_text"), show_highlights=kwargs.get("show_highlights"))
    elif command_type == "answer":
        if format_type == "toon":
            print_toon_answer(data)
        else:
            print_answer(data)
    elif command_type == "research":
        if format_type == "toon":
            print_toon_research(data)
        else:
            print_research_task(data)
